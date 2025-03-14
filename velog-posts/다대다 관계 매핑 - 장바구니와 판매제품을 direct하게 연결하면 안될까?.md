# 다대다 관계 매핑 - 장바구니와 판매제품을 direct하게 연결하면 안될까?
📅 2024-05-22

<p>본격적인 여름프로젝트(SWS)를 진행하기에 앞서, 동아리에서 간단한 프로젝트를 진행하고 있다. </p>
<h2 id="알라딘-중고제품-웹사이트-클론코딩">알라딘 중고제품 웹사이트 클론코딩</h2>
<h3 id="개요">개요</h3>
<ul>
<li>디자인팀이 현재 알라딘 사이트를 리디자인</li>
<li>상품(product)에 대해 여러 중고제품(item)이 존재하는 구조
  ex) &quot;어린왕자&quot;라는 책에 대해 여러 권의 판매하는 중고제품이 존재할 수 있다. 이 중고제품들은 상태, 지점 위치 등이 다르다.</li>
<li>간소화한 부분들이 존재 <ol>
<li>모든 카테고리들을 활성화x - '건강취미'만 접속 가능 </li>
<li>모든 지점들을 활성화x - '전체보기', '신촌점만 보기' </li>
<li>자체 로그인x, 카카오 로그인만 가능</li>
<li>제품등록 기능 구현x </li>
<li>주문 및 결제 기능 구현x<ul>
<li>즉, 있어야 하는 기능들은 다음과 같다: </li>
</ul>
<ol>
<li>카카오 로그인을 통한 회원가입, 로그아웃</li>
<li>리뷰 생성, 한 상품에 대한 리뷰 전체조회, 리뷰 삭제 </li>
<li>장바구니에 제품 추가, 장바구니 제품 전체 조회, 장바구니 단일 제품 삭제</li>
<li>상품 전체 조회, 상품 검색, 상품 상세 조회, 상품타입별(서적/음반/굿즈) 조회</li>
<li>신촌점 메인페이지에서 보여질 제품들 조회(상품타입별 4개씩)</li>
<li>상품상세조회페이지에서 보일 제품 목록 조회</li>
</ol>
</li>
</ol>
</li>
</ul>
<br />

<h3 id="erd">ERD</h3>
<p>작성한 ERD는 다음과 같다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/3a8fdc40-896e-410f-b323-a153ecdb97e6/image.png" /></p>
<h3 id="장바구니와-판매제품을-direct하게-연결하면-안될까">장바구니와 판매제품을 direct하게 연결하면 안될까?</h3>
<p>JPA에서는 다대다 관계를 표현하기 위해 <code>@ManyToMany</code>  를 지원한다. 
그러나, <strong>실무에서는 다음과 같은 이유로 사용하지 않는다.</strong> </p>
<ul>
<li>관계형 데이터베이스는 정규화된 테이블 2개로 다대다 관계를 표현할 수 없다.</li>
<li><code>@ManyToMany</code>를 사용하면 JPA가 자동으로 중간 테이블을 생성해주긴 하지만, 복잡한 조인 쿼리를 발생시켜 개발자가 의도하지 않은 방식으로 작동할 수 있다. </li>
<li><code>@ManyToMany</code>를 사용하면 중간 테이블에 추가 컬럼이 필요한 경우, 추가 데이터를 배핑하지 못한다.</li>
</ul>
<blockquote>
<p>다대다 관계는 일대다, 다대일 관계로 풀어 사용하자!</p>
</blockquote>
<p>연결 테이블 엔티티를 추가하는 셈이다. 
ERD에서 Item과 Cart 사이에 CartItem을 넣어준 것을 확인할 수 있다. </p>
<ul>
<li>Item<pre><code class="language-java">public class Item {    
...            
  @OneToMany(mappedBy = &quot;item&quot;, cascade = CascadeType.ALL, orphanRemoval = true)
  @Builder.Default
  private List&lt;CartItem&gt; cartItems = new ArrayList&lt;&gt;();
...  
</code></pre>
</li>
</ul>
<pre><code>
- Cart
``` java
public class Cart {    
...            
    @OneToMany(mappedBy = &quot;cart&quot;, cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List&lt;CartItem&gt; cartItems = new ArrayList&lt;&gt;();
...  
</code></pre><ul>
<li><p>CartItem</p>
<pre><code class="language-java">@Entity
public class CartItem {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = &quot;cart_item_id&quot;, updatable = false)
  private Long cartItemId;

  // FK
  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = &quot;cart_id&quot;, updatable = false)
  private Cart cart;

  // FK
  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = &quot;item_id&quot;, updatable = false)
  private Item item;
}
</code></pre>
</li>
</ul>
<p>```</p>