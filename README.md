# <font color="red"><center>**AutoVN30-SSI-API-Project**</center></font>
<br></br>


- [**AutoVN30-SSI-API-Project**](#autovn30-ssi-api-project)
  - [**I. Tạo Virtual environment cho project**](#i-tạo-virtual-environment-cho-project)
    - [**Bước 1: Tạo virtual environment**](#bước-1-tạo-virtual-environment)
    - [**Bước 2: Kích hoạt virtual environment**](#bước-2-kích-hoạt-virtual-environment)
    - [**Bước 3:  Cài đặt các thư viện từ requirements.txt**](#bước-3--cài-đặt-các-thư-viện-từ-requirementstxt)
    - [**Bước 4:  Thoát khỏi chế dộ virtual environment**](#bước-4--thoát-khỏi-chế-dộ-virtual-environment)
  - [**II. Các loại lệnh trên thị trường**](#ii-các-loại-lệnh-trên-thị-trường)
    - [**1. Tổng quan**](#1-tổng-quan)
    - [**2. Bảng tóm tắt**](#2-bảng-tóm-tắt)
    - [**3. Chi tiết từng loại lệnh**](#3-chi-tiết-từng-loại-lệnh)
      - [3.1. Lệnh LO – Limit Order](#31-lệnh-lo--limit-order)
      - [3.2. Lệnh ATO – At The Open](#32-lệnh-ato--at-the-open)
      - [3.3. Lệnh ATC – At The Close](#33-lệnh-atc--at-the-close)
      - [3.4. Lệnh MP – Market Price (HOSE)](#34-lệnh-mp--market-price-hose)
      - [3.5. Lệnh MTL – Market To Limit (HNX)](#35-lệnh-mtl--market-to-limit-hnx)
      - [3.6. Lệnh MOK – Market Or Kill (HNX)](#36-lệnh-mok--market-or-kill-hnx)
      - [3.7. Lệnh MAK – Market And Kill (HNX)](#37-lệnh-mak--market-and-kill-hnx)
      - [3.8. Lệnh PLO – Post Limit Order (HNX – lệnh sau giờ)](#38-lệnh-plo--post-limit-order-hnx--lệnh-sau-giờ)
      - [3.9. Lệnh GTD – Good Till Date](#39-lệnh-gtd--good-till-date)




## <font color="blue">**I. Tạo Virtual environment cho project**</font>
### **Bước 1: Tạo virtual environment**
```bash
    python -m venv venv
```

### **Bước 2: Kích hoạt virtual environment**
*Windows (Command Prompt):*  

        venv\Scripts\activate


Windows (PowerShell)

        .\venv\Scripts\Activate.ps1


macOS/Linux

        source venv/bin/activate


### **Bước 3:  Cài đặt các thư viện từ requirements.txt**

        pip install -r requirements.txt


### **Bước 4:  Thoát khỏi chế dộ virtual environment**

        deactivate

<br></br>



## <font color="blue">**II. Các loại lệnh trên thị trường**</font>

### **1. Tổng quan**

Các loại lệnh phổ biến:

- **LO** – Limit Order (Lệnh giới hạn)
- **ATO** – At The Open (Lệnh tại giá mở cửa)
- **ATC** – At The Close (Lệnh tại giá đóng cửa)
- **MP** – Market Price (Lệnh thị trường – HOSE)
- **MTL** – Market To Limit (HNX)
- **MOK** – Market Or Kill (HNX)
- **MAK** – Market And Kill (HNX)
- **PLO** – Post Limit Order (Lệnh sau giờ – HNX)
- **GTD** – Good Till Date (Lệnh giới hạn đến ngày)
---


### **2. Bảng tóm tắt**

| Mã lệnh | Tên              | Có nhập giá? | Loại giá               | Thời gian hiệu lực          | Hành vi khớp / phần còn lại                          |
|---------|------------------|--------------|------------------------|-----------------------------|------------------------------------------------------|
| LO      | Limit Order      | **Có**       | Giá do user nhập       | Trong ngày / đến ngày (GTD) | Khớp từng phần, phần còn lại treo sổ lệnh            |
| ATO     | At The Open      | **Không**    | Giá mở cửa             | Chỉ phiên ATO               | Không khớp thì hủy cuối phiên ATO                    |
| ATC     | At The Close     | **Không**    | Giá đóng cửa           | Chỉ phiên ATC               | Không khớp thì hủy cuối phiên ATC                    |
| MP      | Market Price     | **Không**    | Giá thị trường         | Trong phiên khớp liên tục   | Khớp từng phần, phần còn lại → LO                    |
| MTL     | Market To Limit  | **Không**    | Giá thị trường → Limit | Trong phiên khớp liên tục   | Khớp phần được, phần còn lại → LO                    |
| MOK     | Market Or Kill   | **Không**    | Giá thị trường         | Ngay lập tức                | Không khớp đủ 100% thì hủy toàn bộ                   |
| MAK     | Market And Kill  | **Không**    | Giá thị trường         | Ngay lập tức                | Khớp phần được, phần còn lại hủy                     |
| PLO     | Post Limit Order | **Không**    | Giá đóng cửa           | Phiên sau giờ (15:00–15:15) | Khớp tại giá đóng cửa nếu còn đối ứng, không thì hủy |
| GTD     | Good Till Date   | **Có**       | Giá giới hạn (Limit)   | Đến ngày chỉ định           | Khớp từng phần, phần còn lại treo đến ngày hết hạn   |

---


### **3. Chi tiết từng loại lệnh**

#### 3.1. Lệnh LO – Limit Order

**Ý nghĩa:**  
Lệnh mua/bán tại **mức giá giới hạn** do nhà đầu tư đặt. Chỉ khớp nếu thị trường tồn tại đối ứng với giá phù hợp.

**Đặc điểm:**

- **price_required:** `true`
- **price_type:** `LIMIT`
- **time_in_force:**
  - Trong ngày: `DAY`
  - Kết hợp với GTD: `GTD` + `expire_date`
- **partial_fill:** cho phép khớp từng phần, phần còn lại treo trên sổ lệnh đến hết hiệu lực.
---


#### 3.2. Lệnh ATO – At The Open

**Ý nghĩa:**  
Lệnh dùng trong **phiên khớp lệnh định kỳ xác định giá mở cửa**, không ghi giá cụ thể, được ưu tiên cao hơn lệnh LO.

**Đặc điểm:**

- **price_required:** `false`
- **price_type:** `MARKET_OPEN`
- **session_constraint:** chỉ cho phép gửi trong khung ATO (ví dụ: 09:00–09:15).
- **partial_fill:** có thể khớp từng phần.
- **order_life:** chỉ tồn tại trong phiên ATO; cuối phiên nếu chưa khớp → hủy.
---


#### 3.3. Lệnh ATC – At The Close

**Ý nghĩa:**  
Giống ATO nhưng dùng để khớp **tại giá đóng cửa** trong phiên ATC.

**Đặc điểm:**

- **price_required:** `false`
- **price_type:** `MARKET_CLOSE`
- **session_constraint:** chỉ trong khung ATC (ví dụ HOSE: 14:30–14:45).
- **order_life:** hết ATC mà chưa khớp → hủy.
---


#### 3.4. Lệnh MP – Market Price (HOSE)

**Ý nghĩa:**  
Lệnh mua/bán tại **giá thị trường tốt nhất hiện tại** trên HOSE.

- Mua MP → khớp tại **giá bán thấp nhất** đang chờ.
- Bán MP → khớp tại **giá mua cao nhất** đang chờ.

Nếu không khớp hết, phần còn lại có thể được chuyển thành **LO** theo quy tắc của sàn/CTCK.

**Đặc điểm:**

- **price_required:** `false`
- **price_type:** `MARKET`
- **partial_fill:** cho phép, phần còn lại có thể → LO hoặc hủy tùy quy định.
- **time_in_force:** thường là `IOC` hoặc logic riêng của HOSE (CTCK sẽ quy định).
---


#### 3.5. Lệnh MTL – Market To Limit (HNX)

**Ý nghĩa:**  
- Khớp ngay theo **giá thị trường**.  
- Phần không khớp sẽ được **chuyển thành lệnh LO** với mức giá đã khớp gần nhất.

**Đặc điểm:**

- **price_required:** `false`
- **price_type:** `MARKET_TO_LIMIT`
- **partial_fill:** cho phép.
- **remainder_behavior:** phần dư → LO (limit) và treo trên sổ lệnh.
---


#### 3.6. Lệnh MOK – Market Or Kill (HNX)

**Ý nghĩa:**  
Lệnh thị trường nhưng **hoặc khớp 100%, hoặc không khớp gì** (bị hủy toàn bộ).

**Đặc điểm:**

- **price_required:** `false`
- **price_type:** `MARKET`
- **time_in_force:** tương đương `FOK` (Fill Or Kill).
- **partial_fill:** KHÔNG cho phép; không đủ khối lượng đối ứng → hủy toàn bộ.
---


#### 3.7. Lệnh MAK – Market And Kill (HNX)

**Ý nghĩa:**  
Lệnh thị trường **khớp được bao nhiêu thì khớp**, phần còn lại **hủy luôn**, không treo trên sổ lệnh.

**Đặc điểm:**

- **price_required:** `false`
- **price_type:** `MARKET`
- **time_in_force:** tương đương `IOC` (Immediate Or Cancel).
- **partial_fill:** cho phép, phần còn lại **hủy**.
---


#### 3.8. Lệnh PLO – Post Limit Order (HNX – lệnh sau giờ)

**Ý nghĩa:**  
Lệnh được đặt **sau khi đóng cửa** (phiên PLO, khoảng 15:00–15:15), khớp tại **giá đóng cửa** của phiên chính.

**Đặc điểm:**

- **price_required:** `false` (giá = giá đóng cửa).
- **price_type:** `LIMIT_CLOSE` hoặc `POST_CLOSE` (tùy API).
- **session_constraint:** chỉ cho phép gửi trong phiên PLO.
- **order_life:** hết phiên PLO mà chưa khớp → hủy.
---


#### 3.9. Lệnh GTD – Good Till Date

**Ý nghĩa:**  
Lệnh LO nhưng **có ngày hết hạn cụ thể**. Lệnh sẽ treo trên sổ lệnh từ ngày đặt đến khi:
- Khớp đủ khối lượng, hoặc
- Đến ngày hết hạn, hoặc
- Bị hủy thủ công bởi nhà đầu tư.

**Đặc điểm:**

- **price_required:** `true`
- **price_type:** `LIMIT`
- **time_in_force:** `GTD`
- **expire_date:** bắt buộc.
- **partial_fill:** cho phép; phần chưa khớp tiếp tục treo đến hết hạn.
Markdown All In One