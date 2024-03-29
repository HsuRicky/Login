from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from Member.utils.oauth2.google import startValid, callbackHandler, testSession, revokeAccess
from Member.utils.secure.secureTools import sessionKeyGenerate
from Member.utils.loginSignup.login import loginCheck
from Member.utils.loginSignup.signup import signupCheck

from Login.settings import DEBUG
import json


def login(request):
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'ok': False, 'message': 'Method Not Allowed.'}, status=405)

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        session_public_key, session_private_key = sessionKeyGenerate()
        request.session['login_public_key'] = session_public_key
        request.session['login_private_key'] = session_private_key
        context = {
            "spk_client": session_public_key,
        }
        return render(request, 'member/login.html', context=context)

    # call api to login
    body = json.loads(request.body)

    lc = loginCheck()

    lc.decryptBody(body, request.session['login_private_key'])
    if not lc.lsr.ok:
        return JsonResponse({'ok': lc.lsr.ok, 'message': lc.lsr.message}, status=lc.lsr.code)

    lc.process(loginby="Self")

    if lc.lsr.ok:
        auth.login(request, lc.lsr.user_obj)

    return JsonResponse({'ok': lc.lsr.ok, 'message': lc.lsr.message}, status=lc.lsr.code)


def signup(request):
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'ok': False, 'message': 'Method Not Allowed.'}, status=405)

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        session_public_key, session_private_key = sessionKeyGenerate()
        request.session['signup_public_key'] = session_public_key
        request.session['signup_private_key'] = session_private_key
        context = {
            "spk_client": session_public_key,
        }
        return render(request, 'member/signup.html', context=context)

    body = json.loads(request.body)

    sc = signupCheck()
    sc.decryptBody(body, request.session['signup_private_key'])

    if not sc.lsr.ok:
        return JsonResponse({'ok': sc.lsr.ok, 'message': sc.lsr.message}, status=sc.lsr.code)

    sc.process(signupby="Self")

    return JsonResponse({'ok': sc.lsr.ok, 'message': sc.lsr.message}, status=sc.lsr.code)


def google(request):
    referrer = request.headers.get('Referer')

    if not referrer:
        return JsonResponse({"message": "Forbidden"}, status=403)

    if "/member/login/" in referrer:
        request.session['GoogleOauth2By'] = 'Login'
    elif "/member/signup/" in referrer:
        request.session['GoogleOauth2By'] = 'Signup'
    else:
        return JsonResponse({"message": "Forbidden"}, status=403)

    obj = startValid()
    authorization_url = obj['authorization_url']
    request.session['state'] = obj['state']

    return HttpResponseRedirect(authorization_url)


def google_callback(request):
    state = request.session['state']

    authorization_response = (
        "http://" if DEBUG else "https://") + request.get_host() + request.get_full_path()

    credentials = callbackHandler(
        state, authorization_response)

    obj = testSession(credentials)

    print(obj['userInfos'])

    request.session['credentials'] = obj['credentials']

    try:
        GoogleOauth2By = request.session['GoogleOauth2By']
        if not GoogleOauth2By:
            raise
    except:
        return HttpResponseRedirect('/member/logout/')

    if GoogleOauth2By == 'Login':
        lc = loginCheck()

        lc.oauthSet(obj['userInfos']['email'], obj['userInfos']['id'])

        lc.process(loginby="Google")

        if lc.lsr.ok:
            auth.login(request, lc.lsr.user_obj)
            return HttpResponseRedirect('/')

        return render(request, "member/callback.html", {"GoogleOauth2By": GoogleOauth2By, "fail_reason": lc.lsr.message, "redirect": "/member/login/"})

    if GoogleOauth2By == 'Signup':
        sc = signupCheck()

        sc.oauthSet(obj['userInfos']['name'], obj['userInfos']
                    ['email'], obj['userInfos']['id'])

        sc.process(signupby="Google")

        if sc.lsr.ok:
            auth.login(request, sc.lsr.user_obj)
            return HttpResponseRedirect('/')

        return render(request, "member/callback.html", {"GoogleOauth2By": GoogleOauth2By, "fail_reason": sc.lsr.message, "redirect": "/member/signup/"})

    return HttpResponseRedirect('/member/logout/')


def logout(request):
    if 'credentials' in request.session:
        credentials = request.session['credentials']

        result = revokeAccess(credentials)

    try:
        del request.session['credentials']
    except:
        pass

    auth.logout(request)

    redirect = request.GET.get("redirect")

    if redirect == "/member/login/":
        return HttpResponseRedirect('/member/login/')
    elif redirect == "/member/signup/":
        return HttpResponseRedirect('/member/signup/')

    return HttpResponseRedirect('/member/login/')


@login_required(login_url='/member/login/')
def index(request):
    return HttpResponse("<style>body{background:black} a{color:white}</style><a href='/member/logout/'>logout</a>")