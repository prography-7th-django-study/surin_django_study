# prography-django-study

## 서비스 개요
카페를 즐려 이용하는 사람들을 위한 프랜차이즈 카페 모아보기 서비스 ☕️

## 모델
### 상품
- 이름
- 가격
- 제품 이미지
- 상세 설명
- 영양 정보
- 뜨거운 음료 사이즈
- 차가운 음료 사이즈
(차가운 것과 뜨거운 것으 사이즉 같은 음료라도 다른 경우를 위해 !)
- 한정 음료 종료일
- 카테고리
- 브랜드

### 브랜드
- 이름
- 카테고리(브랜드 별로 카테고리가 상이 할 수 있기 때문)

### 카테고리
- 이름

### 리뷰
- 리뷰 대상 상품
- 내용
- 별점
- 작성자
- 작성된 날짜
- 이미지

## 기능
### 상품
- 스태프일 경우 음료 생성/삭제/수정이 가능하다.
- 음료 대한 리뷰가 존재한다.

### 카테고리
- 카테고리 별로 음료를 모아 볼 수 있다.
- 카테고리 별 음료 순위를 확인 할 수 있다.

### 브랜드
- 브랜드 별로 음료를 모아 볼 수 있다.
- 현위치를 기반으로 가까운 지점을 찾아볼 수 있다.
- 브랜드에 대해 별점으로 평가 가능하다.
- 평가된 별점을 통계로 브랜드 별 순위를 볼 수 있다.
- 브랜드 내의 음료 순위를 확일 할 수 있다.
- 새로운 메뉴를 확인할 수 있다.

### 리뷰
- 음료에 대해 리뷰를 생성/삭제/수정이 가능하다.
- 리뷰는 별점 순으로 정렬하여 볼 수 있다.

