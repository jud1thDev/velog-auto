# CI/CD 파이프라인 구축 (GitHub Actions + AWS Codedeploy + EC2 + RDS + S3)
📅 2024-05-31

<h1 id="ec2-인스턴스">EC2 인스턴스</h1>
<h2 id="ec2-인스턴스-생성">EC2 인스턴스 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/259617fd-61ae-4a84-b575-f0cbc44d5d66/image.png" />
EC2 서비스를 검색해 들어가고, 왼쪽 대시보드에서 인스턴스 메뉴로 들어가 인스턴스 시작 버튼을 클릭합니다.
우측 상단에 표시되는 지역이 서울이 아니라면 서울로 바꿔줍니다.
(AWS 전세계 리전 가운데 가격이 가장 저렴한 리전은 미국의 버지니아 동부 리전이라고 합니다. 서버 응답 시간이 덜 중요한 경우, 비용 절감을 위해 이러한 저렴한 리전을 선택하는 것도 좋은 방법입니다.)
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/59714695-1f0f-4c82-ad6d-3eef3fa5fded/image.png" />
이름은 비어있어도 되나, 저는 'efub-blog'로 설정해주었습니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/d8734dcf-3760-486e-863b-69a978f6de1a/image.png" />
AMI의 경우 저는 Ubuntu를 선택해주었습니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/ea946868-8e1b-4dd5-b3ff-fd721e67c855/image.png" />
인스턴스 유형은 프리티어를 사용중이라 선택권이 없습니다. ㅎㅎ
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/9200dd9e-eb84-4d31-beef-b8094af38f7c/image.png" />
'새 키 페어 생성'을 눌러 EC2서버에 SSH 접속을 하기 윈한 키 페어를 생성해줍시다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/fafbaabf-62a4-4717-9e57-ecedff47f592/image.png" />
원하는 키 페어 이름을 적고, Mac이라면 키 파일 형식을 <code>.pem</code>으로, 윈도우라면 <code>.ppk</code>로 설정해줍니다. '키 페어 생성'을 누르면 자동으로 <code>.pem / .ppk</code>파일이 다운되는데, 한 번 다운받은 후에는 재다운 받을 수 없기 때문에 잘 저장해두도록 합시다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/fbdf862a-b7ad-4ee0-84c8-0056507ded1d/image.png" />
방금 생성한 이름의 키 페어가 잘 선택되어있는 걸 볼 수 있습니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/e31b9853-51a1-4697-8725-9bad4576c425/image.png" />
네트워크 설정을 해줍시다. 
보안 그룹을 별도 생성할 것이라면 SSH 트래픽만 허용해줍시다.
저는 보안 그룹을 별도 생성할 예정입니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/67a77aab-1a6a-40e3-afc3-2c16329fd9c5/image.png" />
볼륨 크기는 30으로 변경, 볼륨 유형은 범융 SSD로 유지시켜줍니다. 볼륨 크기의 경우 프리티어는 최대 30까지 지원합니다. 
만약 볼륨 유형에 프로비저닝된 IOPS SSD를 선택한다면 사용하지 않아도 활성화한 기간만큼 계속 비용이 발생하게 됩니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/bd8b07ff-ad60-463d-aeb8-42594a61e4bd/image.png" />
고급 세부정보는 건드리지 않고, 인스턴스 요약에서 지금까지 올바르게 잘 설정했는지 확인 후 인스턴스 시작을 눌러 인스턴스를 생성합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/9e3fe615-24f3-4a3b-93ad-50486aac0b0f/image.png" />
다시 처음 화면으로 돌아오면 인스턴스가 생성된 것을 확인할 수 있습니다. </p>
<br />

<h2 id="ec2-인스턴스-태그-추가">EC2 인스턴스 태그 추가</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/175156a1-e7d9-4d61-8f9f-6d4dc5843660/image.png" />
이전 화면에서 <strong>인스턴스 ID</strong>를 누른 후, <strong>작업-인스턴스 설정-태그 관리</strong>를 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/25b6548b-76b5-4f3f-a5fe-fc7d8eef6d51/image.png" />
태그 이름을 설정한 후, <strong>저장</strong>을 클릭합니다. </p>
<br />

<h2 id="탄력적-ip">탄력적 IP</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/6c544884-18a3-49a9-88e3-93cbdd036255/image.png" />
EC2서비스에 들어가서, 왼쪽 카테고리의 <strong>네트워크 및 보안</strong>의 <strong>탄력적 IP</strong> 메뉴를 클릭합니다. 그리고 주황색 <strong>탄력적 IP 주소 할당</strong> 버튼을 클릭하면 됩니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/183d5de4-e602-49be-93c1-8d25abdeb6fe/image.png" />
생성된 탄력적 IP 주소를 클릭한 후, 다음과 같은 화면이 뜨면 <strong>탄력적 IP 주소 연결</strong> 클릭해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/10bb1877-090a-43ac-9fd1-cdfe5049076e/image.png" />
연결하려는 EC2 인스턴스를 선택해줍니다. 인스턴스를 선택하면 프라이빗IP는 자동으로 생기는데, 그것도 선택해줍니다.</p>
<h2 id="iam-역할-추가">IAM 역할 추가</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/20bacecf-bb85-4db4-ae7c-4f23da14668b/image.png" />
<strong>IAM 서비스로 이동</strong>한 후, 대시보드에서 <strong>역할 메뉴</strong>로 들어가 <strong>역할 생성</strong>을 클릭해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/afe8bbaf-a9ef-4a05-99ee-aaace72e42c0/image.png" />
신뢰할 수 있는 엔티티 유형에 'AWS 서비스'를, 
사용 사례에 'EC2'를 고른 후 우측 하단의 주황색 <strong>다음</strong>을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/f9542006-de67-4b47-a92b-1a425f8b1b1d/image.png" />
AmazonS3FullAccess를 추가하고 다음으로 넘어갑니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/0be4d3c4-e834-43e3-b1e8-ba2652ee78ad/image.png" />
역할 이름을 작성하고, <strong>역할 생성</strong>을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/aa1adfb2-4fb7-43d2-a2cc-acdc7fa6f9f6/image.png" />
다시 <strong>EC2 서비스 - 인스턴스 메뉴</strong>로 돌아가, 우측 상단의 <strong>작업 - 보안 - IAM 역할 수정</strong>을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/13a7d972-be46-43e0-8457-d7c8c0ea0001/image.png" />
바로 직전에 만들어준 역할을 선택한 후, <strong>IAM 역할 업데이트</strong>를 클릭합니다. </p>
<h1 id="ec2와-rds-연동하기">EC2와 RDS 연동하기</h1>
<h2 id="rds-보안그룹-생성">RDS 보안그룹 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7cb32691-c2e1-4b67-9bb4-176410d3a2f9/image.png" />
EC2서비스로 돌아가, 왼쪽 카테고리에서 <strong>보안 그룹</strong> 메뉴로 들어간 후 <strong>보안 그룹 생성</strong> 버튼을 클릭해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/3ac74605-7247-4f6f-9116-0b7327dad2f7/image.png" />
보안 그룹 이름을 입력한 후, 현재 EC2에서 사용하는 VPC를 선택해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/b709b846-7d10-4223-a0b3-026b92021577/image.png" />
EC2의 VPC ID는 여기서 확인할 수 있습니다. 서브넷 ID도 필요하니 겸사겸사 같이 확인해 줍시다..
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/0679ae08-c644-4eac-89be-7750358a8d3f/image.png" />
보안그룹도 체크해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7a198898-2677-4c8a-873a-990044c33869/image.png" />
다시 돌아와, 방금 체크한 보안그룹을 소스에 넣어줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/de23fb2c-26a0-4737-9568-a1e69318f3bc/image.png" />
EC2 인스턴스로 돌아와 보안그룹에 다음과 같은 인바운드 규칙을 추가해주었습니다. </p>
<br />

<h2 id="rds-서브넷-그룹-생성">RDS 서브넷 그룹 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/ffab6a02-3388-42e0-9558-c228b76534e1/image.png" />
RDS서비스로 들어가서 <strong>서브넷 그룹</strong> 메뉴를 클릭,<strong>DB 서브넷 그룹 생성하기</strong> 버튼을 클릭합니다. (<em>서브넷은 VPC의 IP 주소를 나누어 리소스가 배치되는 물리적인 주소 범위를 의미합니다.)
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/a01f0f7d-e85c-4ee8-9082-05a6e0a6ed58/image.png" />
이름을 적절하게 입력하고, 위에서 확인한 EC2의 VPC를 골라줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/32d5e1ac-53ad-4228-a488-76dc5e7f8571/image.png" />
표시된 것들을 모조리 선택하고 *</em>생성** 버튼을 클릭해줍니다. </p>
<br />

<h2 id="rds-데이터베이스-생성">RDS 데이터베이스 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/14946d53-ed0c-4b33-b74a-a1731cd615aa/image.png" />
RDS 서비스로 들어와, 왼쪽 카테고리에서 데이터베이스 메뉴를 선택한 후, 데이터베이스 생성 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/d5baf102-f567-41e6-bf4f-c45f58f7c138/image.png" />
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/b556324b-324e-4796-a458-6d4fc2674136/image.png" />
사용할 데이터베이스와 적절한 버전 선택하고
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/12fed5ee-87b4-469b-8e63-211507e67f32/image.png" />
프리티어를 골라줬고 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/33245060-6d01-402a-bae8-5a9a55965608/image.png" />
DB 인스턴스 식별자와 마스터 사용자 정보 등록해줍니다.(입력한 사용자 이름과 비밀번호를 잘 기억해둡니다.)
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/6451e8a7-3151-4a48-a476-b265607a9d44/image.png" />
스토리지 유형 gp2 선택해주고, 프리티어의 경우 사용할 수 있는 용량은 20GB까지입니다. 스토리지 자동 조정을 활성화하면 최대 100%까지 무료 백업 스토리지를 제공하지만 혹시 모를 과금 사태를 방지하기 위해 지금은 비활성화로 체크해두겠습니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/c304a3ec-409f-463b-9b78-f1fb2a308b8e/image.png" />
<strong>EC2 컴퓨팅 리소스에 연결 안 함</strong>을 선택해줍니다. EC2 컴퓨팅 리소스에 바로 연결을 선택하면 퍼블릭 액세스를 활성화하지 못합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7678f106-a4b0-4e8b-8166-844f16af5cf1/image.png" />
아까 만든 서브넷 그룹 선택
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/17c3f52a-f775-4f83-85db-9a5b9fc8d672/image.png" />
<strong>퍼블릭 액세스 허용</strong>으로 선택
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7f9f7d77-a162-4f0c-8298-0a643baf11de/image.png" />
뒤에서 EC2와 연결하면서 자동으로 보안그룹이 생성될 것이기에 따로 보안그룹을 생성해주지 않습니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/fea455e1-a4e6-4d60-8658-0bd98ae4ff7a/image.png" />
가용영역도 선택해줍니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/1ba96062-c1e4-4bab-9184-a07a986aaa95/image.png" />
<strong>항상 모니터링 활성화</strong>로 변경
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/55534438-336f-4b5c-a833-3d3343d6db35/image.png" />
추가구성으로 데이터베이스 이름을 지정해주었지만, 기본값을 사용해도 무방합니다. 
설정을 끝마치고, 데이터베이스 생성 버튼을 클릭해줍니다. 데이터베이스 생성에는 시간이 조금 걸립니다.(5분정도) 그 사이에 아래의 과정을 진행합니다. </p>
<br />

<h2 id="rds-파라미터-그룹-생성">RDS 파라미터 그룹 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/6f2981f9-3207-4cfe-b9a1-c496e6413ecc/image.png" />
이번에는 왼쪽 카테고리에서 파라미터 그룹 메뉴로 들어온 후, <strong>파라미터 그룹 생성</strong> 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/e4e874e9-4f45-4ba2-a439-d4244df30f44/image.png" />
적절한 파라미터 그룹 이름과 설명을 입력해주고, 저는 mysql을 사용하므로 다음과 같이 설정하였습니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/b843bdf9-2ad6-4a45-b194-c844dd68cb5c/image.png" />
완성된 파라미터 그룹의 이름을 클릭하면
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/bf0b11ff-d65f-4dd5-a3e9-92ba4422fe37/image.png" />
이런 화면이 뜰텐데, 편집 버튼을 클릭해줍니다. </p>
<ol>
<li>Time_zone : 전부 Asia/Seoul  </li>
<li>character_set : 전부 utf8mb4</li>
<li>collation : 전부 utf8mb4_general_ci
를 적어준 후 변경 사항을 저장해줍니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/2016c682-ca6c-4195-84db-1415fbc15050/image.png" />
다시 RDS 데이터베이스 메뉴로 돌아오면, 데이터베이스가 잘 생성되어있는 걸 확인할 수 있습니다. <strong>데이터베이스 이름</strong>을 클릭하면
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/9546717b-8023-4d5a-91ed-63b85d0c455f/image.png" />
이런 화면이 뜰 텐데, <strong>수정</strong> 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/a16d50ab-9d21-4a88-a1ce-c0a949b36589/image.png" />
추가구성 옵션에서 방금 생성한 파라미터 그룹으로 선택한 후 수정을 완료합니다. </li>
</ol>
<br />

<h1 id="putty">PuTTY</h1>
<h2 id="putty-설치">PuTTY 설치</h2>
<p><a href="https://github.com/iPuTTY/iPuTTY/releases">https://github.com/iPuTTY/iPuTTY/releases</a>
<a href="https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html">https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html</a>
위의 링크에서 PuTTY를 설치합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/329c74c6-e6c8-4df1-96a1-2e4bd77e3abe/image.png" />
AWS의 <strong>EC2서비스- 인스턴스 메뉴</strong>에 들어가 아까 만들어준 <strong>인스턴스ID</strong>를 클릭한 후, IP주소를 복사합니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/58fa9ebf-2380-4009-a7da-366c00bf8b11/image.png" />
PuTTY를 실행 후, 복사한 IP주소를 <strong>Host Name(or IP address)</strong>에 입력
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/92a5cd3e-b4be-4e83-b6b4-c2cb308697b0/image.png" />
왼쪽 카테고리에서** 연결 - SSH - Auth **로 이동한 후, 아까 다운받은 <code>.ppk</code>파일을 선택합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/bd39a151-17d0-4caf-84f3-1b84a169969f/image.png" />
왼쪽 카테고리에서 세션 메뉴로 이동 후, 지금까지의 변경된 설정을 저장하고 열기를 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/751a998e-e994-4a77-b339-a9ee9c576cfb/image.png" />
서버에 설정된 사용자 이름을 입력합니다.</p>
<br />

<h2 id="ec2에-codedeploy-agent-설치">EC2에 CodeDeploy agent 설치</h2>
<pre><code class="language-bash">$ sudo apt update 
$ sudo apt install ruby-full 
$ sudo apt install wget
$ cd /home/ubuntu
$ wget https://aws-codedeploy-ap-northeast-2.s3.ap-northeast-2.amazonaws.com/latest/install
$ chmod +x ./install 
$ sudo ./install auto &gt; /tmp/logfile
$ sudo service codedeploy-agent status</code></pre>
<p>다음 명령어들을 순차적으로 입력해줍니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/a4d3e65b-c4bb-4503-b4d6-cdcdd7fe4769/image.png" />
설치 완료시 다음과 같은 화면이 뜹니다. </p>
<br />

<h2 id="ec2에-java-설치">EC2에 Java 설치</h2>
<pre><code class="language-bash">$ java -version</code></pre>
<p>다음 명령어를 입력해서 java가 설치되어 있는지 확인합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/3475c85b-e45c-4495-9db0-c39b66b9403e/image.png" />
전 없네요...</p>
<pre><code class="language-bash">$ sudo apt update
$ sudo apt install openjdk-17-jdk</code></pre>
<p>그러므로 다음 명령어를 입력하여 JDK17을 설치해줬습니다. 
 <img alt="" src="https://velog.velcdn.com/images/8w8u8/post/c2400669-0943-4fe7-a20c-f4dc6058a15f/image.png" />
설치 후 다시 <code>$ java -version</code> 를 입력해 확인해줍니다.</p>
 <br />


<h2 id="ec2-timezone-설정">EC2 Timezone 설정</h2>
<pre><code class="language-bash">$ sudo timedatectl set-timezone Asia/Seoul</code></pre>
<p>기본 서버 시간이 미국이므로, 다음 명령어를 입력하여  시스템의 시간대가 Asia/Seoul로 설정되도록 합니다. </p>
<pre><code class="language-bash">$ date</code></pre>
<p>date 명령어로 시간이 잘 설정되었는지 확인해줍니다.</p>
 <br />


<h2 id="ec2-mysql-설치">EC2 MySQL 설치</h2>
<pre><code class="language-bash">$ sudo apt-get install mysql-server</code></pre>
<p>다음 명령어를 입력해 mysql을 설치해줍니다. </p>
<br />

<h1 id="mysql-데이터베이스-생성">mysql 데이터베이스 생성</h1>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/bad14f3f-71e1-49f6-be96-7c6871129a92/image.png" /></p>
<ul>
<li>SSH Hostname: EC2 Public IPv4</li>
<li>SSH Username: ubuntu</li>
<li>SSH Password: X</li>
<li>SSH Key File: EC2 <strong>pem</strong> 파일</li>
<li>MySQL Hostname: RDS 엔드포인트</li>
<li>Username: DB username</li>
<li>Password: DB password</li>
</ul>
<br />


<h1 id="s3-버킷-생성">S3 버킷 생성</h1>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/2b0521cd-14bc-474c-8b18-9cbe4f410730/image.png" /></p>
<p>S3 서비스로 들어가 <strong>버킷만들기</strong>를 클릭합니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/15be5042-ba24-45fa-9f71-95ec3c581aea/image.png" />
버킷 이름을 설정해주고 <strong>버킷만들기</strong>를 클릭합니다.</p>
<br />

<h1 id="iam">IAM</h1>
<h2 id="codedeploy를-위한-iam-역할-생성">CodeDeploy를 위한 IAM 역할 생성</h2>
<p> CodeDeploy를 위한 IAM역할을 생성하려고 합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/a5f5d486-b2c2-48e5-8331-d5003451f373/image.png" />
IAM 서비스로 들어와 욈쪽에서 <strong>역할</strong> 메뉴 클릭, <strong>역할 생성</strong>버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/adc42bb9-8409-4821-9911-43417175fb28/image.png" />
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/d58e4601-00af-4260-a281-3d9f1dc627e2/image.png" />
위와 같이 설정하고, <strong>다음</strong>버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/3b07f53b-6c1c-4cf7-85ba-7001607fe455/image.png" />
<strong>다음</strong>
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/ed527965-d51f-4a44-bf7a-f847da3c5984/image.png" />
<strong>역할 생성</strong> 버튼을 클릭합니다. </p>
<br />

<h2 id="codedeploy-애플리케이션-생성">CodeDeploy 애플리케이션 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/f41df710-774b-437a-a06b-ab8f43019059/image.png" />
CodeDeploy 서비스로 이동해서, 왼쪽 카테고리에서 <strong>애플리케이션</strong> 메뉴로 들어가 <strong>애플리케이션 생성</strong> 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/38d9981a-78bc-40fb-9481-2df7b65d8eb5/image.png" />
이름을 적절하게 입력하고, 컴퓨팅 플랫폼은 <strong>EC2/온프레미스</strong>를 선택한 후 <strong>애플리케이션 생성</strong> 버튼을 클릭합니다. </p>
<br />

<h2 id="codedeploy-배포-그룹-생성">CodeDeploy 배포 그룹 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/8f297861-9a18-486e-9042-debbba2bc137/image.png" />
<strong>배포 그룹 생성</strong> 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7998fadb-8b18-4aa0-9365-6d2f4f2eeac7/image.png" />
적절한 배포 그룹 이름을 입력한 후 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/ff3c64b8-dbb0-4f7d-8ec3-d23c6d620fd5/image.png" />
아까 생성한 IAM역할 선택
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/d40cf4b1-cfb9-412e-a486-1c38633470d8/image.png" />
환경구성에서는 EC2 인스턴스에 추가한 태그를 선택해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/072dc013-cc3c-4c1b-8075-b5c609ea572e/image.png" />
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/b9450799-c4b8-4316-b423-60caea6f6941/image.png" />
다음과 같이 설정해주고, <strong>배포 그룹 생성</strong> 버튼을 클릭합니다. </p>
<br />

<h2 id="github-actions를-위한-iam-사용자-생성">GitHub Actions를 위한 IAM 사용자 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/d7fa2de4-f2c2-4514-aeb8-b23db7156012/image.png" />
IAM서비스로 다시 돌아가서, <strong>사용자</strong> 메뉴로 들어간 후 <strong>사용자 생성</strong> 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/49fb5627-30b4-49d4-af1e-caf6f512e901/image.png" />
이름을 적절하게 입력하고 다음 클릭
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/061f2c99-acd6-403d-be4a-442b24d5204a/image.png" />
권한 옵션에 <strong>직접 정책 연결</strong> 선택
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/9ca45c45-a3ac-4db7-bacc-43794be96f00/image.png" />
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/ae60005b-cebf-45a4-98ce-26a963615b73/image.png" />
<strong>codedeployfull</strong>과 <strong>s3full</strong>을 추가해준 후 다음 버튼을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/586cb524-315f-44b2-9f56-0a924078cce6/image.png" />
올바르게 설정했는지 확인 후 <strong>사용자 이름</strong>을 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/fa01c522-1ca5-4495-917b-9af741ae0a4e/image.png" />
<strong>보안 자격 증명</strong> 탭에 들어간 후 <strong>액세스 키 만들기</strong>를 클릭합니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/57a5dbd7-f0d9-464f-9d9d-4af27339fcd5/image.png" />
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/e104817c-a070-4df0-bf93-1a1ad5cef9d9/image.png" />
다음과 같이 설정 후 <strong>액세스 키 만들기</strong> 버튼을 클릭합니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/e2bf78d9-28b3-45c1-8e42-c97ae230f1de/image.png" /> 
액세스 키가 생성되었습니다. 지금이 아니면 csv파일을 다운받을 수 없으니 다운받아 잘 저장해둡시다.</p>
<br />

<h1 id="github-sercret에-iam-사용자-액세스-키-정보-추가">GitHub Sercret에 IAM 사용자 액세스 키 정보 추가</h1>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7169b1c2-86f2-4a76-a4bc-40d29966f492/image.png" />
깃허브 리포지토리 설정에서 repository secret을 추가해줍니다.</p>
<ul>
<li>AWS_ACCESS_KEY_ID</li>
<li>AWS_SECRET_ACCESS_KEY
이 두개는 방금 다운받은 액세스 키 csv파일에서 정보를 확인하고 입력해줍니다.</li>
<li>APPLICATION_YML<pre><code class="language-yaml">spring:
datasource:
  driver-class-name: com.mysql.cj.jdbc.Driver
  url: jdbc:mysql://{RDS 엔드포인트}:3306/{DB명}?createDatabaseIfNotExist=true&amp;characterEncoding=UTF-8&amp;characterSetResults=UTF-8
  username: {DB username}
  password: {DB password}
jpa:
  hibernate:
    ddl-auto: update
  generate-ddl: true
  show-sql: true</code></pre>
</li>
</ul>
<br />

<h2 id="appspecyml-작성">appspec.yml 작성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/308410cc-6735-46b7-89f6-504802e3a77f/image.png" /></p>
<p>appspec.yml 파일을 추가하고, 아래처럼 작성해줍니다.</p>
<pre><code class="language-yaml">version: 0.0
os: linux

files:
  - source: /
    destination: /home/ubuntu/{root_directory_name}
    overwrite: yes
file_exists_behavior: OVERWRITE

permissions:
  - object: /
    pattern: &quot;**&quot;
    owner: ubuntu
    group: ubuntu

hooks:
  AfterInstall:
    - location: scripts/stop.sh
      timeout: 60
      runas: ubuntu

  ApplicationStart:
    - location: scripts/start.sh
      timeout: 60
      runas: ubuntu</code></pre>
<br />

<h2 id="배포-스크립트-작성">배포 스크립트 작성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7bfbabb0-49d0-4485-b24a-2d34eeaa5d67/image.png" />
<code>scripts</code> 패키지를 생성하고, <code>stop.sh</code>, <code>start.sh</code> 파일을 작성해줍니다. </p>
<ul>
<li><code>stop.sh</code><pre><code class="language-shell">#!/usr/bin/env bash
</code></pre>
</li>
</ul>
<p>PROJECT_ROOT=&quot;/home/ubuntu/{root_directory_name}&quot;
JAR_FILE=&quot;$PROJECT_ROOT/blog-webapp.jar&quot;</p>
<p>DEPLOY_LOG=&quot;$PROJECT_ROOT/deploy.log&quot;</p>
<p>TIME_NOW=$(date +%c)</p>
<h1 id="현재-구동-중인-애플리케이션-pid-확인">현재 구동 중인 애플리케이션 PID 확인</h1>
<p>CURRENT_PID=$(pgrep -f $JAR_FILE)</p>
<h1 id="프로세스가-켜져-있으면-종료">프로세스가 켜져 있으면 종료</h1>
<p>if [ -z $CURRENT_PID ]; then
  echo &quot;$TIME_NOW &gt; 현재 실행 중인 애플리케이션이 없습니다.&quot; &gt;&gt; $DEPLOY_LOG
else
  echo &quot;$TIME_NOW &gt; 실행 중인 $CURRENT_PID 애플리케이션 종료&quot; &gt;&gt; $DEPLOY_LOG
  kill -15 $CURRENT_PID
fi</p>
<pre><code>- ```start.sh```
``` shell 
#!/usr/bin/env bash

PROJECT_ROOT=&quot;/home/ubuntu/{root_directory_name}&quot;
JAR_FILE=&quot;$PROJECT_ROOT/blog-webapp.jar&quot;

APP_LOG=&quot;$PROJECT_ROOT/application.log&quot;
ERROR_LOG=&quot;$PROJECT_ROOT/error.log&quot;
DEPLOY_LOG=&quot;$PROJECT_ROOT/deploy.log&quot;

TIME_NOW=$(date +%c)

# build 파일 복사
echo &quot;$TIME_NOW &gt; $JAR_FILE 파일 복사&quot; &gt;&gt; $DEPLOY_LOG
cp $PROJECT_ROOT/build/libs/*.jar $JAR_FILE

# jar 파일 실행
echo &quot;$TIME_NOW &gt; $JAR_FILE 파일 실행&quot; &gt;&gt; $DEPLOY_LOG
nohup java -jar $JAR_FILE &gt; $APP_LOG 2&gt; $ERROR_LOG &amp;

CURRENT_PID=$(pgrep -f $JAR_FILE)
echo &quot;$TIME_NOW &gt; 실행된 프로세스의 아이디는 $CURRENT_PID 입니다.&quot; &gt;&gt; $DEPLOY_LOG</code></pre><br />

<h2 id="applicationyml-파일-수정">application.yml 파일 수정</h2>
<pre><code class="language-yaml">spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://{RDS 엔드포인트}:3306/{DB명}?createDatabaseIfNotExist=true&amp;characterEncoding=UTF-8&amp;characterSetResults=UTF-8
    username: {DB username}
    password: {DB password}
  jpa:
    hibernate:
      ddl-auto: update
    generate-ddl: true
    show-sql: true</code></pre>
<br />

<h2 id="buildgradle-파일-수정">build.gradle 파일 수정</h2>
<p>빌드 시 -plain.jar 파일이 생기지 않도록 다음 코드를 build.gradle에 추가해줍니다. </p>
<pre><code class="language-java">jar {
    enabled = false
}</code></pre>
<br />

<h2 id="github-actions-workflow-작성">GitHub Actions Workflow 작성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/43fc9955-a14e-4572-9635-c1a2b8add503/image.png" />
actions 탭에 들어가 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/dcbb9dc4-6075-4ac9-967b-7aaeb9213486/image.png" />
<code>deploy.yml</code> 파일을 생성해줍니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/3fe8f042-7c07-4ac5-aa05-68ee5d97a0b9/image.png" />
이 위치에 생성이 되어야해요!</p>
<pre><code class="language-yaml">name: Deploy to Amazon EC2

on:
  push:
    branches: [ &quot;{브랜치명}&quot; ]

env:
  AWS_REGION: ap-northeast-2
  S3_BUCKET_NAME: {S3 버킷명}
  CODE_DEPLOY_APPLICATION_NAME: {CodeDeploy 애플리케이션명}
  CODE_DEPLOY_DEPLOYMENT_GROUP_NAME: {CodeDeploy 배포 그룹명}

permissions:
  contents: read

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: make application.yml
        run: |
          mkdir ./blog/src/main/resources 
          cd ./blog/src/main/resources
          touch ./application.yml
          echo &quot;${{ secrets.APPLICATION_YML }}&quot; &gt; ./application.yml

      - name: Build with Gradle
        run: |
          cd blog
          chmod +x ./gradlew
          ./gradlew build -x test

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Upload to AWS S3
        run: |
          aws deploy push \
            --application-name ${{ env.CODE_DEPLOY_APPLICATION_NAME }} \
            --ignore-hidden-files \
            --s3-location s3://$S3_BUCKET_NAME/$GITHUB_SHA.zip \
            --source ./blog

      - name: Deploy to AWS EC2 from S3
        run: |
          aws deploy create-deployment \
            --application-name ${{ env.CODE_DEPLOY_APPLICATION_NAME }} \
            --deployment-config-name CodeDeployDefault.AllAtOnce \
            --deployment-group-name ${{ env.CODE_DEPLOY_DEPLOYMENT_GROUP_NAME }} \
            --s3-location bucket=$S3_BUCKET_NAME,key=$GITHUB_SHA.zip,bundleType=zip</code></pre>
<br />

<h1 id="각종-에러들">각종 에러들</h1>
<p>다채롭게 오류가 많았던 실습이었습니다ㅎㅎㅠ </p>
<h2 id="타임아웃-에러--ec2-인스턴스-인바운드-규칙-문제">타임아웃 에러 : EC2 인스턴스 인바운드 규칙 문제</h2>
<p>이건 그냥 포트 8080, 80 규칙으로 잘 넣어주면 됨! 위에서 서술한 내용 참고해주세요.</p>
<h2 id="could-not-connect-the-ssh-tunnel">could not connect the SSH tunnel</h2>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/3afb8a69-6825-4971-9162-84c2373d9216/image.png" /></p>
<p>cmd에서 <code>ssh -i</code> 명령어로 SSH서버에 접속하여 </p>
<pre><code>ED25519 key fingerprint is SHA256:5Dqrj98XFN8NCBTFA03Ec9w4/KWqI4It67HuShqNHj4.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes</code></pre><p>yes를 눌러주어서 해결</p>
<h2 id="error-connect-econnrefused">Error: connect ECONNREFUSED</h2>
<h3 id="원인1---codedeploy-실패">원인1 - CodeDeploy 실패</h3>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/33a23712-080f-452a-a44f-47f6db77affb/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/976f2232-662a-4686-9a4d-84c5f5c0e548/image.png" /></p>
<p>깃허브 액션에서는 문제가 없었는데.. 
도대체 왜!!!! 서버와 연결이 안되는 것인가?ㅠㅠ</p>
<p>인터넷에 찾아도 저 에러 메세지에 대해서는 별다른 도움을 얻을 수 없었어요.. 인바운드 규칙 수정이나 방화벽을 살펴보라는데, 저는 그 문제가 아니였습니다. </p>
<p>그러던 중 AWS CodeDeploy서비스에 들어갔더니 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/bb234e9e-f1e2-49a9-ba61-644429d6b993/image.png" /></p>
<p>수많은 실패의 흔적들과 (인스턴스랑 데이터베이스 설정을 잘못했나 싶어서 여러 번 만들고 연결하고 반복하느라 그런듯)</p>
<blockquote>
<p>The overall deployment failed because too many individual instances failed deployment, too few healthy instances are available for deployment, or some instances in your deployment group are experiencing problems.</p>
</blockquote>
<p>이런 에러가 있었습니다. 구글링을 해보니 </p>
<p><a href="https://github.com/jojoldu/freelec-springboot2-webservice/issues/80">https://github.com/jojoldu/freelec-springboot2-webservice/issues/80</a></p>
<p>이런 감사한 글을 발견했습니다...
codedeploy-agent 로그 파일을 확인할 수 있다는것을 알게되어 PuTTY로 접근해 확인해 보니, </p>
<blockquote>
<p>ERROR [codedeploy-agent(2453)]: InstanceAgent::Plugins::Code              DeployPlugin::CommandPoller: Error during perform: Aws::S3::Errors::PermanentRed              irect - The bucket you are attempting to access must be addressed using the spec              ified endpoint. Please send all future requests to this endpoint.</p>
</blockquote>
<p>이런 에러가 있었는데요. 
S3 버킷도 다른 region에 만들어버려서 생긴 문제라네요.</p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/629f8635-b153-44e8-b0ce-b2ad1d4067de/image.png" />
...... 진짜 얘 왜 시드니에 있죠? 
서울에서 다시 생성해줬습니다.ㅋㅋㅠ</p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/94e18ae4-a486-4e92-97cf-d99acda5f6f2/image.png" /></p>
<p>이제 aws codedeploy에서는 성공적으로 실행되고 있네요. </p>
<h3 id="원인-2---telnet-unable-to-connect-to-remote-host-connection-refused">원인 2 - telnet: Unable to connect to remote host: Connection refused</h3>
<p>그런데도 여전히 서버와 연결 안 되는 문제가 발생했는데요.</p>
<p>SSH 접속 후 </p>
<pre><code class="language-BASH">telnet {도착지서버} {포트번호}</code></pre>
<p>로 확인해보면</p>
<pre><code>//계속 대기 중이면 방화벽 오픈이 안된 상태
telnet {도착지서버} {포트번호}
Trying {도착지서버}...

//방화벽 오픈 되었으나 연결 거부
telnet {도착지서버} {포트번호}
Trying {도착지서버}...
telnet: Unable to connect to remote host: Connection refused

//정상적으로 방화벽 오픈이 되었고, 통신할 준비가 되어있는 경우
telnet {도착지서버} {포트번호}
Trying {도착지서버}...
Connected to {도착지서버}
Escape character is '^]'.</code></pre><p>이 세 가지 응답 중 하나를 받을 수 있습니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/069f66f9-a75c-4ffd-a941-347e1b32f030/image.png" />
저는 두번째 응답을 받았습니다. 
8080 포트에서 애플리케이션이 수신 대기 중이지 않다는 것인데요.</p>
<blockquote>
<p>즉, Spring Boot 애플리케이션이 정상적으로 실행되지 않았거나 실행되었더라도 8080 포트에서 수신하지 않고 있어서입니다.</p>
</blockquote>
<p>먼저, <code>ps aux | grep java</code> 명령어로 Java 프로세스가 실행 중인지 확인해봅니다. 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/82d07293-6c8d-4c54-8481-38b397257be0/image.png" />
Java 프로세스가 실행중이지 않은 걸 확인할 수 있었습니다.
이렇게 되면, <code>.jar</code> 파일이 있는 위치로 이동한 후 어플리케이션을 수동으로 실행해봐야합니다. 저는 테스트 코드를 안 짰으므로, <code>gradlew.bat build -x test</code> 명령어로 테스트를 건너뛰고 빌드해주었습니다.</p>
<p>jar파일이 빌드 시 만들어지려면, <code>build.gradle</code> 에서</p>
<pre><code>jar {
    enabled = true
}</code></pre><p>와 같이 true로 설정해주어야 합니다.</p>
<pre><code>// jar파일이 생성됐는지 디렉토리에서 확인
cd C:/Users/정유정/Desktop/efub4-backend-session/blog/build/libs

// jar 파일 서버로 전송
scp -i &quot;{jar파일 경로}&quot; ubuntu@{도착지 서버}:/home/ubuntu/

// 어플리케이션 실행
ssh -i {pem파일 경로} ubuntu@{도착지 서버}:/home/ubuntu/
java -jar {jar 파일명}</code></pre><p>jar 파일이 생성되면, 우분투 서버로 전송해준 후 어플리케이션을 실행해줍니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/1a6f08cc-a827-4806-a3db-61a57643c6d9/image.png" />
이제 서버와 잘 연결되는 걸 확인할 수 있습니다.</p>
<hr />
<p>참고</p>
<ul>
<li><p><a href="https://bcp0109.tistory.com/356">https://bcp0109.tistory.com/356</a></p>
</li>
<li><p><a href="https://velog.io/@softwarerbfl/AWS-EC2-RDS-%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0">https://velog.io/@softwarerbfl/AWS-EC2-RDS-%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0</a></p>
</li>
<li><p><a href="https://velog.io/@ncookie/EC2-RDS-%EC%9D%B8%EC%8A%A4%ED%84%B4%EC%8A%A4-%EC%83%9D%EC%84%B1-%EB%B0%8F-%EC%97%B0%EB%8F%99">https://velog.io/@ncookie/EC2-RDS-%EC%9D%B8%EC%8A%A4%ED%84%B4%EC%8A%A4-%EC%83%9D%EC%84%B1-%EB%B0%8F-%EC%97%B0%EB%8F%99</a></p>
</li>
<li><p><a href="https://velog.io/@pds0309/EC2-key%EB%A1%9C-ssh%EC%A0%91%EC%86%8D-Permission-Denied-public-key-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0">https://velog.io/@pds0309/EC2-key%EB%A1%9C-ssh%EC%A0%91%EC%86%8D-Permission-Denied-public-key-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0</a></p>
</li>
<li><p><a href="https://junspapa-itdev.tistory.com/32">https://junspapa-itdev.tistory.com/32</a></p>
</li>
</ul>