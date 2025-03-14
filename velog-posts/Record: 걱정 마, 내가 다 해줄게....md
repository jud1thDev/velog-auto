# Record: 걱정 마, 내가 다 해줄게...
📅 2024-11-03

<p>객체 생성 시 반복되는 필드 선언, 생성자 작성 등에 지치셨나요.. <del>(인텔리제이 자동 생성 단축키가 있긴 하지만)</del>
Record DTO를 활용하여 코드를 간결하게 작성해봅시다. </p>
<h1 id="불변-객체의-장점과-한계">불변 객체의 장점과 한계</h1>
<p>불변 객체는 데이터를 변경할 수 없어 유지보수에 유리하지만, 객체 생성 시 필드 선언과 다양한 메서드 구현에 많은 Boilerplate 코드가 필요합니다. 이는 유지보수 시 필드 추가나 수정 시 모든 Boilerplate 코드를 수정해야 하는 번거로움을 초래합니다.</p>
<h1 id="boilerplate-코드란">Boilerplate 코드란?</h1>
<p>Boilerplate 코드란, 프로그래밍에서 특정 작업을 수행하기 위해 반복적으로 사용되는 코드입니다. 예를 들어, 객체 생성 시 필드 선언, 생성자, equals, hashCode, <strong>getter</strong> 등을 매번 정의하는 작업을 의미합니다.</p>
<h1 id="레코드의-도입-배경">레코드의 도입 배경</h1>
<p>레코드는 이러한 Boilerplate 코드 문제를 해결하기 위해 도입되었습니다. 레코드를 사용하면 간단한 한 줄 정의로 불변 객체의 기능을 모두 갖춘 데이터를 표현할 수 있습니다. (필드 정의와 함께 자동으로 생성자, equals, hashCode, toString 등을 제공)</p>
<h1 id="레코드의-사용">레코드의 사용</h1>
<p>레코드에서 정의된 필드는 모두 불변이고 인스턴스 생성 시 함께 선언되어야 하기 때문에 <strong>인스턴스 필드를 나중에 추가하거나 변경할 수 없습니다.</strong> </p>
<p>그러나 예외적으로 <strong>static 필드</strong>는 인스턴스의 상태와 무관하게 클래스 전체에 걸쳐 공유되는 필드이기 때문에 레코드에서도 추가할 수 있습니다.</p>
<p>기본 메서드(equals, hashCode, toString)는 재정의하여 원하는 대로 수정할 수도 있습니다.</p>
<pre><code class="language-java">public record Person(String name, String address) {
    static final String DEFAULT_COUNTRY = &quot;Korea&quot;;

    @Override
    public String toString() {
    return &quot;사람입니다.&quot;

}</code></pre>
<p>레코드는 일반 객체처럼 new 키워드로 생성할 수 있으나, 차이점은 필드값 접근 시 <strong>get 접두사 없이</strong> 직접 접근합니다. </p>
<pre><code class="language-java">// RequestDto
public record FriendCreateRequestDto(
        @NotNull Long friendRequestId) {
        // 전 new 키워드로 객체를 생성하는 방식보다 
        // toEntity() 메서드로 DTO에서 객체를 생성하는 방식을 선호합니다.
    public Friend toEntity(User sender, User receiver) {
        return Friend.builder()
                .user1(receiver)
                .user2(sender)
                .build();
    }
}

// Service
User receiver = userService.getActiveUserByUserId(requestDto.receiverId());</code></pre>
<p>예를 들어, 위의 서비스 코드에서 receiverId 필드는 getReceiverId()가 아닌 receiverId() 형태로 사용됩니다.</p>
<h1 id="레코드와-일반-객체와의-비교">레코드와 일반 객체와의 비교</h1>
<p>예시 코드를 통해 레코드와 일반 객체를 비교하며, 레코드의 편리함을 설명해보겠다. </p>
<pre><code class="language-java">import lombok.Getter;

@Getter
public class Person {
    private final String name;
    private final String address;

    public Person(String name, String address) {
        validate(name, address);
        this.name = name;
        this.address = address;
    }

    private void validate(String name, String address) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException(&quot;Name cannot be empty&quot;);
        }
        if (address == null || address.isBlank()) {
            throw new IllegalArgumentException(&quot;Address cannot be empty&quot;);
        }
    }
}</code></pre>
<pre><code class="language-java">// 1. getter 혹은 get메서드 정의 필요 없음 
public record Person(String name, String address) {

// 2. 컴팩트한 생성자 : 파라미터 생략 가능
    public Person {
        validate(name, address); 
        // 3. 필드 초기화는 자동으로 처리됨 (this.name = name 같은 할당 필요 없음)
    }

    private void validate(String name, String address) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException(&quot;Name cannot be empty&quot;);
        }
        if (address == null || address.isBlank()) {
            throw new IllegalArgumentException(&quot;Address cannot be empty&quot;);
        }
    }
}</code></pre>
<br />

<h1 id="레코드와-lombok-비교">레코드와 Lombok 비교</h1>
<p>레코드와 Lombok은 유사한 역할을 하지만 차이점이 있습니다:</p>
<ul>
<li>가독성: 레코드가 더 간결함.</li>
<li>의존성: Lombok은 외부 라이브러리를 설치해야 하지만 레코드는 자바 JDK 16 이상에서 바로 사용 가능.</li>
<li>유연성: Lombok은 다양한 기능을 제공함.</li>
</ul>
<p>복잡한 객체에서는 Lombok이 더 유리할 수 있습니다. 상황에 따라 레코드의 간결함을 택할지, Lombok의 유연성을 택할지 결정하면 됩니다.</p>
<h1 id="레코드를-도메인-객체에-사용할-수-있는가">레코드를 도메인 객체에 사용할 수 있는가?</h1>
<p>레코드는 단순히 불변 데이터를 전달하기 위한 캐리어로, 비즈니스 로직을 포함하는 도메인 객체에는 적합하지 않습니다. 
<strong>레코드는 도메인 객체보다는 DTO와 같은 단순 데이터 전달 객체에 사용하는 것이 적합합니다.</strong></p>
<hr />
<p>참고
<a href="https://www.youtube.com/watch?v=MiHxFpTgAog">https://www.youtube.com/watch?v=MiHxFpTgAog</a></p>