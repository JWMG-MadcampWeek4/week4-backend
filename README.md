![1](https://github.com/JWMG-MadcampWeek4/week4-backend/assets/149568715/42a4ef0b-fdd3-4301-9cf2-86b63c54541b)
![2](https://github.com/JWMG-MadcampWeek4/week4-backend/assets/149568715/01cf190d-14b0-467d-8622-606998f5fe6c)



# ShortsMaker

## Make shorts to show

---

- 해싱을 도입한 자체 로그인을 구현했습니다.
- 사용자가 여태 까지 만든 쇼츠를 볼 수 있는 창을 구현했습니다.
- 쇼츠의 주제, 내용, 대본, 음성, 이미지의 생성까지 웹에서 전부 해결할 수 있도록 구현했습니다.

---

### a. 개발 팀원

2023W 몰입캠프 Week 3 1분반

- 서재원 - 한양대학교 컴퓨터소프트웨어학부 22학번
- 강민구 - KAIST 수리과학 19학번

---

### b. 개발 환경

- Language : React, Typescript, Flask
- DB : MongoDB
- target : web
- IDE : Visual Studio Code

---

### c. 웹 소개

### Login/Signup

![KakaoTalk_Photo_2024-01-26-14-22-59 001](https://github.com/JWMG-MadcampWeek4/week4-frontend/assets/149568715/9ee51301-fabc-4e3a-87e2-8afa6842b173)

### Major Features

- signup 창에서는 아이디, 비밀번호, 닉네임 입력받습니다. 중복검사를 지원합니다.
- login 창에서 db에 저장되어 있는 아이디와 비밀번호를 입력하면 메인화면으로 이동합니다.

### 기술 설명

- signup 시 hash를 이용해서 암호화된 비밀번호를 db에 저장합니다.

### main page
![KakaoTalk_Photo_2024-01-26-14-23-00 002](https://github.com/JWMG-MadcampWeek4/week4-frontend/assets/149568715/a7419632-22df-4eeb-a6ec-1d55f5335522)

### Major Features

- main page에서는 사용자가 여태까지 만든 쇼츠의 링크를 scroll View로 볼 수 있습니다.
- 자신이 만든 쇼츠의 링크를 입력하여 scroll View에 추가할 수 있습니다.

### 기술 설명

- collection_Url에 저장된 shorts link들을 id로 참조하여 DB로부터 불러왔습니다.

### theme
![KakaoTalk_Photo_2024-01-26-14-23-43 002](https://github.com/JWMG-MadcampWeek4/week4-frontend/assets/149568715/40b423f8-9bed-4495-897d-a6378940d4f3)
### Major Features

- 사용자가 만들고 싶은 shorts의 theme과 category를 정하면, content를 추천해줍니다.
- 추천이 잘 되는 theme(수학,과학,역사,동물등)을 사용자에게 제시합니다.
- 추천받고 싶은 category를 사용자가 직접 입력할 수 있습니다.
- 추천받은 content를 수정할 수 있습니다.
- content를 기반으로 script를 만들 수 있습니다.

### 기술 설명

- langchain을 이용해서 만든 자체 chatmodel 함수에 theme을 전달하면, 쇼츠의 content로 적합한 요소들을 5개 찾아 리턴합니다.
- 요소들을 띄우면, 사용자가 원하는 content를 선택합니다.

### script

![KakaoTalk_Photo_2024-01-26-14-23-43 002](https://github.com/JWMG-MadcampWeek4/week4-frontend/assets/149568715/8320848e-6d12-406d-aa2c-bed0cf00649f)

### Major Features

- 만들고 싶은 쇼츠의 content를 기반으로 script를 작성해줍니다.
- 작성된 script는 수정할 수 있습니다.
- 발표시간계산 기능이 있어, 예상 발표시간이 1분 이내가 되도록 script를 수정할 수 있게 했습니다.
- script를 기반으로 이미지를 생성할 수 있습니다.
- script를 읽는 TTS 음성파일을 생성해주고, 다운로드할 수 있습니다.

### 기술 설명

- langchain을 사용하여 만든 자체 chatmodel 함수에 content를 전달하면, 쇼츠에 활용할 수 있는 script를 리턴합니다.
- 발표시간 계산은 단어의 수를 기준으로 발표시간의 추정치를 계산하는 내부 함수를 이용했습니다.
- 제작한 스크립트는 수정하여 다시 TTS를 생성할 수 있습니다.

### image

![Image_all](https://github.com/JWMG-MadcampWeek4/week4-frontend/assets/149568715/05ffa1ea-4822-4569-aebe-b3fa19bc5251)
![Image_sole](https://github.com/JWMG-MadcampWeek4/week4-frontend/assets/149568715/488aae7a-aef2-4be8-9be7-323ed5bda635)
### Major Features

- 대본의 내용에 맞게, 이미지를 총 12개 생성해줍니다.
- 이미지를 생성할때 사용되었던 keyword를 사용자에게 보여주고, 사용자가 이미지가 맘에 들지 않는다면 keyword를 수정해서 이미지를 재생성할 수 있습니다.
- 각각의 이미지를 다운로드할 수도 있고, 전체 이미지를 일괄적으로 다운로드할 수 있습니다.
- 실제 이미지가 모바일에서 어떻게 보이는지 직접 확인해볼 수 있습니다.

### 기술 설명

- langchain을 사용하여 만든 자체 함수에 script를 전달하면, 이미지 생성에 필요한 단어를 추출하여 생성합니다.
- 생성된 단어를 stability ai의 SDXL model의 api를 사용해서 만든 자체 함수에 prompt로 전달하여 이미지를 생성합니다.
- 생성한 이미지를 base64의 형태로 encoding, decoding하여 화면에 보여줍니다.
