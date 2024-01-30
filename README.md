# Login
>  利用 Django 透過前後端分離的架構及模組化設計的登入系統，最後在加上**OAuth 2.0 手動串接Google登入認證**。
  
# 概述  
### **簡介** 
>  學習和理解 OAuth 2.0的 工作原理，開發具有現代化用戶認證系統的應用，手動定制 OAuth 2.0 不僅能強化安全性，同時也能提供更多控制權。  
>  透過直接實作 OAuth 2.0，讓我更深入地瞭解 OAuth 2.0 協議和 Django 框架如何交互工作。有助於我在未來遇到相關問題時，能夠更加迅速和有效地解決。
      
### **Database** 
>  使用 MySQL ，亦可使用 MongonDB。
      
### **安全性**  
>  利用 RSA 非對稱加密加密加密金鑰，並使用對稱加密算法（AES）加密，讓資訊更加安全。  
>  檔案放置於 [..\Member\utils\secure](https://github.com/HsuRicky/Login/tree/main/Login/Member/utils/secure)，可自行參考程式碼。
  
