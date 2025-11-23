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
  - [**III. Đặt lệnh giao dịch**](#iii-đặt-lệnh-giao-dịch)
    - [**1. Request Body**](#1-request-body)
    - [**2. Giải thích các tham số trong API**](#2-giải-thích-các-tham-số-trong-api)
      - [2.1 `instrumentID` – Mã chứng khoán / Hợp đồng tương lai](#21-instrumentid--mã-chứng-khoán--hợp-đồng-tương-lai)
      - [2.2 `market` – Thị trường](#22-market--thị-trường)
      - [2.3 `buySell` – Mua hay bán](#23-buysell--mua-hay-bán)
      - [2.4 `orderType` – Loại lệnh](#24-ordertype--loại-lệnh)
      - [2.5 `channelID`](#25-channelid)
      - [`price`](#price)
      - [2.6 `quantity`](#26-quantity)
      - [2.7 `account`](#27-account)
      - [2.8 `requestID`](#28-requestid)
      - [2.9 `stopOrder`](#29-stoporder)
      - [2.10 `stopPrice`](#210-stopprice)
      - [2.11 `stopType`](#211-stoptype)
      - [2.12 `stopStep` / `profitStep`](#212-stopstep--profitstep)
      - [`code`](#code)
      - [2.13 `deviceId`](#213-deviceid)
      - [2.14 `userAgent`](#214-useragent)




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

## <font color="blue">**III. Đặt lệnh giao dịch**</font>
### **1. Request Body**

```json
{
  "instrumentID": "VN30F1M",
  "market": "VNFE",
  "buySell": "B",
  "orderType": "LO",
  "channelID": "TA",
  "price": 21000,
  "quantity": 300,
  "account": "0901351",
  "stopOrder": false,
  "stopPrice": 0,
  "stopType": "string",
  "stopStep": 0,
  "lossStep": 0,
  "profitStep": 0,
  "requestID": "16781953",
  "code": "123456789",
  "deviceId": "8C-EC-4B-D3-0B-96",
  "userAgent": "FCTrading"
}
```

### **2. Giải thích các tham số trong API**

#### 2.1 `instrumentID` – Mã chứng khoán / Hợp đồng tương lai
- Mã sản phẩm giao dịch: cổ phiếu (SSI, FPT, TCB...) hoặc phái sinh (VN30F1M...).

#### 2.2 `market` – Thị trường
- `VN`: thị trường cơ sở.
- `VNFE`: thị trường phái sinh.

#### 2.3 `buySell` – Mua hay bán
- `B`: Buy (Long). Kỳ vọng giá chỉ số sẽ TĂNG. Mở vị thế mua.
- `S`: Sell (Short). Kỳ vọng giá chỉ số sẽ GIẢM. Mở vị thế bán.

#### 2.4 `orderType` – Loại lệnh
- Xem tai phan: [**II. Các loại lệnh trên thị trường**](#ii-các-loại-lệnh-trên-thị-trường)

#### 2.5 `channelID`
- `TA`: FastConnect Trading API. Luôn đặt "TA" khi giao dịch qua API FCTrading.

#### `price`
- Lệnh LO → price > 0.
- Lệnh khác LO → price = 0.

#### 2.6 `quantity`
- Cơ sở: số cổ phiếu (bội số 100).
- Phái sinh: số hợp đồng (1, 2, ...).

#### 2.7 `account`
- Tài khoản đặt lệnh phù hợp thị trường VN hoặc VNFE.

#### 2.8 `requestID`
- 8 số, duy nhất trong ngày. Bắt buộc duy nhất trong ngày. Dùng để truy vết và chống trùng lệnh.

#### 2.9 `stopOrder`
- `false`: lệnh thường.
- `true`: lệnh điều kiện (phái sinh).
- `stopOrder`, `stopPrice`, `stopType` (Bo Lệnh điều kiện/Dừng)
Đây là nhóm thông số quan trọng để đặt các lệnh quản lý rủi ra và chốt lời/lỗ tự động. Chỉ áp dụng khi stopOrder = true.

#### 2.10 `stopPrice`
- Giá kích hoạt lệnh điều kiện. Khi giá thị trường chạm mức này, lệnh chính (lệnh LO hoặc MP) của bạn sẽ được kích hoạt.

#### 2.11 `stopType`
- Loại điều kiện kích hoạt.
  - `D`: Down. Lệnh dừng bán (Stop Loss). Kích hoạt khi giá GIẢM XUỐNG chạm hoặc vượt qua `stopPrice`. Ví dụ: Bạn đang nắm giữ vị thế Mua (Long) VN30F2406 ở giá 21000. Bạn đặt lệnh điều kiện stopType="D", stopPrice=20800, orderType="LO", price=20790. Khi giá thị trường giảm xuống 20800, lệnh bán LO tại 20790 sẽ được kích hoạt để cắt lỗ.
  - `U`: Up. Lệnh dừng mua (Buy Stop). Kích hoạt khi giá TĂNG LÊN chạm hoặc vượt qua `stopPrice`. Ví dụ: Bạn kỳ vọng sau khi phá vỡ kháng cự 21200, giá sẽ tăng mạnh. Bạn đặt lệnh điều kiện stopType="U", stopPrice=21200, orderType="LO", price=21210. Khi giá thị trường tăng lên 21200, lệnh mua LO tại 21210 sẽ được kích hoạt.
  - `O`: OCO - One Cancels the Other: Cho phép đặt hai lệnh điều kiện cùng lúc (ví dụ: 1 lệnh chốt lời và 1 lệnh cắt lỗ). Khi một lệnh được kích hoạt, lệnh kia sẽ tự động hủy.
  - `V`: Trailing Up.
  - `E`: Trailing Down.
  - `B`: BullBear.

#### 2.12 `stopStep` / `profitStep`
- Áp dụng cho BullBear - stopType = "B". Đây là một loại lệnh phức tạp, kết hợp cả chốt lời và cắt lỗ dựa trên "bước giá".
- `stopStep`: Số bước giá cho lệnh cắt lỗ.
- `profitStep`: Số bước giá cho lệnh chốt lời.
- Ví dụ: Giá tham chiếu là 21000, bước giá là 0.1. Nếu đặt profitStep=10 và stopStep=5, lệnh chốt lời sẽ ở mức 21000 + (10 * 0.1) = 21001, và lệnh cắt lỗ ở 21000 - (5 * 0.1) = 20999.5.

#### `code`
- PIN/OTP giao dịch.
- Nếu xác thực người dùng isSave = false → bắt buộc nhập OTP/PIN.
- Dùng để xác thực lệnh trong hệ thống SSI.

#### 2.13 `deviceId`
- Định danh thiết bị gửi lệnh.

#### 2.14 `userAgent`
- Tác nhân người dùng.