{% extends "base.html" %}

{% block content %}
	
	{%if is_input_error %}整数を入力してください<br>{% endif %}
	<div id="input_form">
	<form action="/damage.html" method="post">
		ダメージ	
		<input class="number" type="number" name="damage" min="0" value ="0"></input>
		同時発射数（武器）
		<input class="number" type="number" name="synchro_num" min="1" value ="1"></input>
		リロード時間（武器）
		<input class="number" type="number" name="reload" min="1" value = "1"></input>
		<input type="submit" value="Submit">
	</form>
	</div>

	{% if has_result %}
		DPS：{{ dps }}<br>
	{% endif %}

	<p>簡易なDPS計算ができます。<br>
	射撃安定性などによるリロードの変化や爆発ダメージは考慮されていないので、参考程度にしてください。<br>
	ダメージは敵に実際に与えたダメージを入力してください。武器の攻撃力とは違います。<br>
	同時発射数はショットガンや３連射バトルライフルを利用するときに入力してください。</p>
	<p>
	計算式：ダメージ×同時発射数÷リロード×60
	</p>

{% endblock %}
