# RESTful 쇼핑몰 상품 관리 API

## 📚 프로젝트 개요
Django REST Framework(DRF)를 사용하여 쇼핑몰의 상품 관리 API를 구현한 프로젝트입니다.  
이 프로젝트는 상품 리스트 조회, 카테고리별 상품 필터링, 상품 상세 정보 제공, 쿠폰 적용 등의 기능을 제공합니다.

---

## 주요 기능
1. **상품 리스트 조회 API**
   - 전체 상품 리스트를 반환합니다.
   - 카테고리별로 상품을 필터링할 수 있습니다.

2. **상품 상세 정보 API**
   - 특정 상품의 상세 정보를 반환합니다.
   - 상품에 할인율 및 쿠폰 적용 유무를 계산하여 원래가격, 할인가격, 최종가격을 반환합니다.

3. **카테고리 리스트 API**
   - 전체 카테고리 정보를 반환합니다.

4. **쿠폰 리스트 API**
   - 전체 쿠폰 정보를 반환합니다.

---

## 🛠️ 기술 스택
- **언어**: Python 3.9
- **프레임워크**: Django 3.0.11, Django REST Framework(DRF) 3.15.1
- **데이터베이스**: MySQL 8.0
- **기타**: python-dotenv (환경 변수 관리)

---

## 📂 프로젝트 구조
```
shopping-mall-api/
├── products/                # 상품 및 관련 모델, 뷰, 시리얼라이저, 유틸
├── shopping_mall/           # 프로젝트 설정 파일
├── manage.py                # Django 관리 스크립트
├── requirements.txt         # 의존성 패키지 목록
└── README.md                # 프로젝트 문서
```

---

## 📦 설치 및 실행

1. **저장소 클론**
   ```bash
   git clone https://github.com/helixous/shopping-mall-api.git
   cd shopping-mall-api
   ```

2. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **의존성 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **환경 변수 설정**
   - `.env` 파일에 다음 키값들을 매핑하여 서빙:
     ```
     SECRET_KEY
     DB_NAME
     DB_USER
     DB_PASSWORD
     DB_HOST
     DB_PORT
     ```

5. **데이터베이스 마이그레이션**
   ```bash
   python manage.py migrate
   ```

6. **서버 실행**
   ```bash
   python manage.py runserver
   ```

---

## 📝 주요 API 명세

### 1. 상품 리스트 조회
- **URL**: `/products/`
- **Method**: `GET`
- **Query Params**:
  - `category_id` : 특정 카테고리 ID로 필터링.
- **Response**:
  ```json
  {
      "status": 200,
      "message": "Success",
      "data": [
          {
              "id": 1,
              "name": "Laptop",
              "price": 1500000,
              "discounted_price": 1350000,
              "category": "Electronics",
              "coupon_applicable": true
          }
      ]
  }
  ```

### 2. 상품 상세 조회
- **URL**: `/products/<int:pk>/`
- **Method**: `GET`
- **Query Params**:
  - `coupon_code` : 적용할 쿠폰 코드.
- **Response**:
  ```json
  {
      "status": 200,
      "message": "Success",
      "data": {
          "id": 1,
          "name": "Laptop",
          "original_price": 1500000,
          "discounted_price": 1350000,
          "final_price": 1215000,
          "is_coupon_applied": true,
          "category": "Electronics",
          "coupon_applicable": true
      }
  }
  ```

### 3. 카테고리 리스트 조회
- **URL**: `/products/categories/`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "status": 200,
      "message": "Success",
      "data": [
          {
              "id": 1,
              "name": "Electronics"
          },
          {
              "id": 2,
              "name": "Fashion"
          }
      ]
  }
  ```

### 4. 쿠폰 리스트 조회
- **URL**: `/products/coupons/`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "status": 200,
      "message": "Success",
      "data": [
          {
              "id": 1,
              "code": "SUMMER21",
              "discount_rate": 0.2
          },
          {
              "id": 2,
              "code": "WINTER21",
              "discount_rate": 0.15
          }
      ]
  }
  ```

---

## 🧪 테스트 방법
- **Postman** 또는 **cURL** 또는 DRF 내장 Browsable API를 사용하여 API를 테스트할 수 있습니다.
- 예: 상품 리스트 조회
  ```bash
  curl -X GET "http://127.0.0.1:8000/products/" -H "accept: application/json"
  
