// var total=document.getElementById("total-count").title;
//                     console.log('Total members:', total);


var total=document.getElementById("total-count").title;
    console.log(total)

// サンプルデータ（名前と滞在時間）
var data = [];
for (let i = 1; i <= total; i++) {
    read_name=document.getElementById(`name-${i}`).title;
    // console.log(read_name);  // 名前を表示
    read_monthly_total_time=document.getElementById(`monthly_total_time-${i}`).title;
    // console.log(read_monthly_total_time);  // 滞在時間を表示
    data.push({ name: read_name, duration: read_monthly_total_time });
};

//テスト用
// var data = [
//     { name: 'a', duration: 150 },
//     { name: 'b', duration: 90 },
//     { name: 'c', duration: 150 },
//     { name: 'd', duration: 80 },
//     { name: 'e', duration: 90 },
//     { name: 'f', duration: 100 }
//     ];

// データを滞在時間が長い順にソート
data.sort((a, b) => b.duration - a.duration);
// テーブルのtbody要素を取得
const tableBody = document.getElementById('ranking-table');

// ソートされたデータをテーブルに追加
var tmp_duartion = 0;
var rank = 1;
data.forEach((item, index) => {
    const row = document.createElement('tr');
                                
    if(item.duration != tmp_duartion){
        rank = index + 1;
    }
    tmp_duartion = item.duration
    row.innerHTML = `
        <td class="rank${rank}">${rank}</td>
        <td class="rank${rank}">${item.name}</td>
        <td class="rank${rank}">${parseInt(item.duration)}h</td>
        `;
    tableBody.appendChild(row);
    // line 46: <td class="rank${rank}">${parseInt(item.duration)/60}h</td>
})

let tabs = document.querySelectorAll("input[name=tabset]");
let tab_check = 'tab1';
for(let tab of tabs) {
    tab.addEventListener('change',function(){
		if( this.checked ) {
			console.log(this.value);
            tab_check = this.value;
            localStorage.setItem('current', tab_check)
		}
	});
    ;
       
}

  


window.onload=function(){
    var currentTab = localStorage.getItem('current');
    console.log(currentTab);
    if (currentTab) {
        for(let tab of tabs) {
            if(tab.value == currentTab){
                tab.checked = true;
            }
            else{
                tab.checked = false;
            }
        }
    }

}




// Submitボタン
document.getElementById("submit_btn").addEventListener('click', function() {
    console.log("!");

});