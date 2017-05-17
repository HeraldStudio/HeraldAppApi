//一周内访问总数折线图
//点击某天后的出现
	//每小时访问数  折线图
	//ios_version 饼状图
	//android 版本分布 饼状图
	//微信端,移动端分布 饼状图
	//每个api访问数 柱状图
	//总请求数

var currentIndex, //当前渲染的第几天的索引
	contents,	//存储7天的访问情况
	week = {},
	api,
	ios_distribute=[],
	android_distribute=[],
	device_distribute=[];

var week_chart = echarts.init(document.getElementById('week'));
var api_chart = echarts.init(document.getElementById("api_order"));
var ios_chart = echarts.init(document.getElementById('ios_version'));
var android_chart = echarts.init(document.getElementById('android_version'));
var hour_chart = echarts.init(document.getElementById('hour'));
var device_chart = echarts.init(document.getElementById('device_distribute'));

inital();

function transformDate(date){
	var y = date.getFullYear();
	var m = date.getMonth()+1;
	var d = date.getDate();
	if(m<10)
		m = '0'+m;
	else
		m+='';
	if(d<10)
		d = '0'+d;
	return y+m+d;
}

function inital(){
	week_chart.showLoading();
	
	var date = new Date();
	date.setDate( date.getDate()-7 );
	
	$.ajax({
		url: 'http://139.129.4.159:7000/herald/api/v1/log',
		type: 'POST',
		dataType: 'json',
		data: {
			date_start: transformDate(date),
			date_cnt: 7},
		timeout: 6000
	})
	.success(function(data){

		week_chart.showLoading();

		contents = data['content'];

		filter();

		currentIndex = contents.length-1
		var date = contents[currentIndex]['date'] + '';
		title.innerHTML = date.slice(0,4)+'年'+date.slice(4,6)+'月'+date.slice(6,8)+'日'+'的具体访问情况';

		inital_week_chart();
		inital_api_chart(currentIndex);
		inital_ios_chart(currentIndex);
		inital_android_chart(currentIndex);
		inital_hour_chart(currentIndex);
		inital_device_chart(currentIndex);

		week_chart.hideLoading();
		console.log( contents );
	})
	.fail(function() {
		console.log('request error');
	});
}

function updateDayInfo(i){
	inital_api_chart(i);
	inital_hour_chart(i);
	inital_ios_chart(i);
	inital_android_chart(i);
	inital_device_chart(i);
}

function filter(){
	for(var i in contents){
		delete contents[i]['ios_version']['null'];
		for( var j in contents[i]["api_order"])
				if(contents[i]["api_order"][j] < 1000)
					delete contents[i]["api_order"][j];
	}
}

function inital_week_chart(){
	for(var i in contents){
		week[ contents[i]["date"] ] = contents[i]["call_count"];
	}

	week_chart.setOption({
		title: {
	    	text: '7天内调用次数变化',
	    	x: 'center',
			y:'top',
			fontSize: "1em"
		},
		tooltip: {
			trigger: "axis"
		},
		xAxis: {
		    data: Object.keys(week)
		},
		yAxis: {},
		series: [{
		    name: '调用次数',
		    type: 'line',
		    data: Object.values(week),
		    markPoint: {
				data: [
					{type: 'max', name: '最大值'},
					{type: 'min', name: '最小值'}
				]
			},
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
		}],
		toolbox: {		//工具箱设定
			show : true,
			orient: 'horizontal',      
			x: 'right',
			y: 'top',
			color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
			backgroundColor: 'rgba(0,0,0,0)',
			borderColor: '#ccc',
			borderWidth: 0,
			padding: 5,
			showTitle: true,
			feature : {
				mark : {
					show : true,
					title : {
						mark : '辅助线-开关',
						markUndo : '辅助线-删除',
						markClear : '辅助线-清空'
			        },
					lineStyle : {
						width : 1,
						color : '#1e90ff',
						type : 'dashed'
					}
				},
				dataView : {
					show : true,
					title : '数据视图',
					readOnly: true,
					lang : ['数据视图', '关闭', '刷新'],
					optionToContent: function(opt) {
						var axisData = opt.xAxis[0].data;
						var series = opt.series;
						var table = '<table style="width:100%;text-align:center"><tbody><tr>'
									+ '<td>时间</td>'
									+ '<td>' + series[0].name + '</td>'
									+ '</tr>';
						for (var i = 0, l = axisData.length; i < l; i++) {
							table += '<tr>'
									+ '<td>' + axisData[i] + '</td>'
									+ '<td>' + series[0].data[i] + '</td>'
									+ '</tr>';
						}
						table += '</tbody></table>';
						return table;
					}
				},
				magicType: {
					show : true,
						title : {
						line : '切换-折线图',
						bar : '切换-柱形图',
					},
					type : ['line', 'bar']
				},
				saveAsImage : {
					show : true,
					title : '保存',
					type : 'jpg',
					lang : ['点击本地保存'] 
				}
			}
		}
	});

}

function inital_api_chart(i){

	api = contents[i]['api_order'];
	api_chart.setOption({
		title: {
	    	text: 'API调用情况(没有展示数量较少的)',
	    	x: 'left',
			y:'top'
		},
		tooltip: {},
		xAxis: {
		    data: Object.keys(api),
		    axisLabel:{
		    	interval: 0
		    }
		},
		yAxis: {},
		series: [{
		    name: '调用次数',
		    type: 'bar',
		    data: Object.values(api)
		}],
		toolbox: {		//工具箱设定
			show : true,
			orient: 'horizontal',      
			x: 'right',
			y: 'top',
			color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
			backgroundColor: 'rgba(0,0,0,0)',
			borderColor: '#ccc',
			borderWidth: 0,
			padding: 5,
			showTitle: true,
			feature : {
				mark : {
					show : true,
					title : {
						mark : '辅助线-开关',
						markUndo : '辅助线-删除',
						markClear : '辅助线-清空'
			        },
					lineStyle : {
						width : 1,
						color : '#1e90ff',
						type : 'dashed'
					}
				},
				dataView : {
					show : true,
					title : '数据视图',
					readOnly: true,
					lang : ['数据视图', '关闭', '刷新'],
					optionToContent: function(opt) {
						var axisData = opt.xAxis[0].data;
						var series = opt.series;
						var table = '<table style="width:100%;text-align:center"><tbody><tr>'
									+ '<td>API</td>'
									+ '<td>' + series[0].name + '</td>'
									+ '</tr>';
						for (var i = 0, l = axisData.length; i < l; i++) {
							table += '<tr>'
									+ '<td>' + axisData[i] + '</td>'
									+ '<td>' + series[0].data[i] + '</td>'
									+ '</tr>';
						}
						table += '</tbody></table>';
						return table;
					}
				},
				saveAsImage : {
					show : true,
					title : '保存',
					type : 'jpg',
					lang : ['点击本地保存'] 
				}
			}
		}
	});
}

function inital_ios_chart(i){
	var temp = contents[i]['ios_version'];
	ios_distribute.length = 0;

	for(var t in temp){
		ios_distribute.push({value: temp[t], name:t});
	}

	ios_chart.setOption({
			title: {
				text: 'iOS端版本分布',
				x: 'left',
				y:'top'
			},
			tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
            	x:'left',
            	y: 'bottom',
            	data: Object.keys(temp)
            },
		    series : [
		        {
		            name: '调用次数(百分比)',
		            type: 'pie',
		            radius: '55%',
		            data: ios_distribute
		        }
		    ],
		    toolbox: {		//工具箱设定
			show : true,
			orient: 'horizontal',      
			x: 'right',
			y: 'top',
			color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
			backgroundColor: 'rgba(0,0,0,0)',
			borderColor: '#ccc',
			borderWidth: 0,
			padding: 5,
			showTitle: true,
			feature : {
				mark : {
					show : true,
					title : {
						mark : '辅助线-开关',
						markUndo : '辅助线-删除',
						markClear : '辅助线-清空'
			        },
					lineStyle : {
						width : 1,
						color : '#1e90ff',
						type : 'dashed'
					}
				},
				saveAsImage : {
					show : true,
					title : '保存',
					type : 'jpg',
					lang : ['点击本地保存'] 
				}
			}
		}
	});
}

function inital_android_chart(i){
	var temp = contents[i]['android_version'];
	android_distribute.length = 0;

	if(temp['']){
		temp['<7']=temp[''];
		delete temp[''];
	}

	for(var t in temp){
		android_distribute.push({value: temp[t], name:t});
	}

	android_chart.setOption({
			title: {
				text: 'Android端版本分布',
	    		x: 'left',
	    		y: 'top'
			},
			tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
            	y: 'bottom',
            	x:'center',
            	data: Object.keys(temp)
            },
		    series : [
		        {
		            name: '调用次数(百分比)',
		            type: 'pie',
		            radius: '55%',
		            data:android_distribute
		        }
		    ],
		    toolbox: {		//工具箱设定
				show : true,
				orient: 'horizontal',      
				x: 'right',
				y: 'top',
				color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
				backgroundColor: 'rgba(0,0,0,0)',
				borderColor: '#ccc',
				borderWidth: 0,
				padding: 5,
				showTitle: true,
				feature : {
					mark : {
						show : true,
						title : {
							mark : '辅助线-开关',
							markUndo : '辅助线-删除',
							markClear : '辅助线-清空'
				        },
						lineStyle : {
							width : 1,
							color : '#1e90ff',
							type : 'dashed'
						}
					},
					saveAsImage : {
						show : true,
						title : '保存',
						type : 'jpg',
						lang : ['点击本地保存'] 
					}
				}
			}
	});
}

function inital_hour_chart(i){
	hour = contents[i]['every_hour_count'];
	hour_chart.setOption({
		title: {
	    	text: '一天内每小时的调用次数变化',
	    	x:'left',
	    	y:'top'
		},
		tooltip: {
			trigger: "xAxis"
		},
		xAxis: {
		    data: Object.keys(hour)
		},
		yAxis: {},
		series: [{
		    name: '调用次数',
		    type: 'line',
		    data: Object.values(hour),
		    markPoint: {
				data: [
					{type: 'max', name: '最大值'},
					{type: 'min', name: '最小值'}
				]
			},
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
		}],
		toolbox: {		//工具箱设定
			show : true,
			orient: 'horizontal',      
			x: 'right',
			y: 'top',
			color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
			backgroundColor: 'rgba(0,0,0,0)',
			borderColor: '#ccc',
			borderWidth: 0,
			padding: 5,
			showTitle: true,
			feature : {
				mark : {
					show : true,
					title : {
						mark : '辅助线-开关',
						markUndo : '辅助线-删除',
						markClear : '辅助线-清空'
			        },
					lineStyle : {
						width : 1,
						color : '#1e90ff',
						type : 'dashed'
					}
				},
				dataView : {
					show : true,
					title : '数据视图',
					readOnly: true,
					lang : ['数据视图', '关闭', '刷新'],
					optionToContent: function(opt) {
						var axisData = opt.xAxis[0].data;
						var series = opt.series;
						var table = '<table style="width:100%;text-align:center"><tbody><tr>'
									+ '<td>时间</td>'
									+ '<td>' + series[0].name + '</td>'
									+ '</tr>';
						for (var i = 0, l = axisData.length; i < l; i++) {
							table += '<tr>'
									+ '<td>' + axisData[i] + '</td>'
									+ '<td>' + series[0].data[i] + '</td>'
									+ '</tr>';
						}
						table += '</tbody></table>';
						return table;
					}
				},
				saveAsImage : {
					show : true,
					title : '保存',
					type : 'jpg',
					lang : ['点击本地保存'] 
				}
			}
		}
	});
}

function inital_device_chart(i){
	var temp= contents[i]['device_distribute'];
	device_distribute.length = 0;
	
	for(var t in temp){
		device_distribute.push({value: temp[t], name:t});
	}

	device_chart.setOption({
			title: {
				text: '设备分布',
				x: 'left',
				y:'top'
			},
			tooltip : {
				trigger: 'item',
				formatter: "{a} <br/>{b} : {c} ({d}%)"
			},
			legend: {
				data: Object.keys(temp),
				y: 'bottom',
				x:'center'
            },
			series : [
				{
                    name:'调用次数(百分比)',
                    type:'pie',
                    data:device_distribute
                }
			],
			toolbox: {		//工具箱设定
				show : true,
				orient: 'horizontal',      
				x: 'right',
				y: 'top',
				color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
				backgroundColor: 'rgba(0,0,0,0)',
				borderColor: '#ccc',
				borderWidth: 0,
				padding: 5,
				showTitle: true,
				feature : {
					mark : {
						show : true,
						title : {
							mark : '辅助线-开关',
							markUndo : '辅助线-删除',
							markClear : '辅助线-清空'
				        },
						lineStyle : {
							width : 1,
							color : '#1e90ff',
							type : 'dashed'
						}
					},
					saveAsImage : {
						show : true,
						title : '保存',
						type : 'jpg',
						lang : ['点击本地保存'] 
					}
				}
			}
	});
}

week_chart.on('click', function (params) {
	if (params.componentType === 'series' && params.seriesType === 'line'){
            var i = params['dataIndex'];
            if( i!=currentIndex ){
				currentIndex=i;
				var date = params.name;
				title.innerHTML = date.slice(0,4)+'年'+date.slice(4,6)+'月'+date.slice(6,8)+'日'+'的具体访问情况';
            	updateDayInfo(i);
            }
        }
});