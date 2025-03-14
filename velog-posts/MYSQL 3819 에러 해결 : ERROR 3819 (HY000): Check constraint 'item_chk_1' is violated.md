# MYSQL 3819 에러 해결 : ERROR 3819 (HY000): Check constraint 'item_chk_1' is violated
📅 2024-05-22

<p> 지금 하고 있는 프로젝트에서는 상품 및 제품 등록 기능을 따로 만들지 않았기에, example data set을 DB에 따로 넣어줘야 했다. </p>
<h3 id="문제">문제</h3>
<p>item에 데이터를 Insert 하던 도중 만난 에러 문구는 다음과 같다. </p>
<pre><code class="language-SQL">  ERROR 3819 (HY000): Check constraint 'item_chk_1' is violated </code></pre>
<h3 id="해결">해결</h3>
<pre><code class="language-SQL">SELECT * FROM {데이터베이스이름}.{테이블이름}; 
SHOW CREATE TABLE {테이블이름}; // 제약조건 확인</code></pre>
<p>제약조건을 확인했을 떄, <strong>테이블의 특정 컬럼(productType)이 between 0 and 1 값을 가져야한다는 제약조건</strong>이 걸려 있었다. productType은 BOOK, RECORD, GOODS 중에 하나를 받도록 ENUM컬럼으로 잘 설정해놨는데 왜 이런 제약 조건이 있지? </p>
<p>원인은 <strong>처음에 실수로 <code>@Enumerated</code> 를 빼먹었어서</strong> 기본적으로 ORDINAL모드로 지정이 되며 저런 제약 조건이 생겼던 것이었다. </p>
<p>ALTER TABLE을 통해 제약조건을 새로 변경해줘도 되고, 나같은 경우는 제약조건을 그냥 드랍했다. </p>
<pre><code class="language-SQL">ALTER TABLE {테이블이름} DROP CONSTRAINT {제약조건};</code></pre>