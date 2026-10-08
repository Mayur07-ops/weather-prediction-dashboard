/**
 * charts.js
 * ─────────────────────────────────────────────────────────────
 * Initialises all 7 ECharts instances for the weather pipeline dashboard.
 * Depends on: weatherData.js (must be loaded first), ECharts CDN.
 *
 * Charts:
 *  1. tempChart       — Monthly temperature range (line)
 *  2. rainChart       — Monthly rainfall & humidity (bar + line)
 *  3. tempDistChart   — Max temp distribution (bar)
 *  4. humDistChart    — Humidity distribution (bar)
 *  5. cloudChart      — Cloud cover distribution (bar)
 *  6. windChart       — Wind gust direction frequency (horizontal bar)
 *  7. rainPieChart    — Rain Today / Tomorrow (donut)
 */

/* ── Shared theme tokens ── */
const BORDER  = '#1f2937';
const MUTED   = '#4b5563';
const TEXT    = '#e2e8f0';
const BLUE    = '#3b82f6';
const CYAN    = '#06b6d4';
const VIOLET  = '#8b5cf6';
const AMBER   = '#f59e0b';
const ROSE    = '#f43f5e';

const TOOLTIP = { backgroundColor: '#131720', borderColor: '#2d3748', textStyle: { color: TEXT } };
const LEGEND  = { textStyle: { color: MUTED }, itemWidth: 10, itemHeight: 10 };

/* ── 1. Monthly Temperature Range ── */
function initTempChart() {
  const chart = echarts.init(document.getElementById('tempChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP, trigger: 'axis' },
    legend: { ...LEGEND, top: 0 },
    grid: { top: 28, right: 18, bottom: 28, left: 38 },
    xAxis: {
      type: 'category', data: MONTHS,
      axisLine: { lineStyle: { color: BORDER } },
      axisTick: { show: false },
      axisLabel: { color: MUTED, fontSize: 10 },
    },
    yAxis: {
      type: 'value', name: '°C',
      nameTextStyle: { color: MUTED, fontSize: 9 },
      splitLine: { lineStyle: { color: BORDER, type: 'dashed' } },
      axisLabel: { color: MUTED, fontSize: 10 },
    },
    series: [
      {
        name: 'Max Temp', type: 'line', smooth: true, symbol: 'circle', symbolSize: 4,
        data: AVG_MAX_TEMP,
        lineStyle: { color: ROSE, width: 2 }, itemStyle: { color: ROSE },
        areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1, colorStops:[{offset:0,color:'rgba(244,63,94,0.2)'},{offset:1,color:'rgba(244,63,94,0)'}] } },
      },
      {
        name: 'Min Temp', type: 'line', smooth: true, symbol: 'circle', symbolSize: 4,
        data: AVG_MIN_TEMP,
        lineStyle: { color: CYAN, width: 2 }, itemStyle: { color: CYAN },
        areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1, colorStops:[{offset:0,color:'rgba(6,182,212,0.12)'},{offset:1,color:'rgba(6,182,212,0)'}] } },
      },
    ],
  });
  return chart;
}

/* ── 2. Monthly Rainfall & Humidity ── */
function initRainChart() {
  const chart = echarts.init(document.getElementById('rainChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP, trigger: 'axis' },
    legend: { ...LEGEND, top: 0 },
    grid: { top: 28, right: 50, bottom: 28, left: 42 },
    xAxis: {
      type: 'category', data: MONTHS,
      axisLine: { lineStyle: { color: BORDER } },
      axisTick: { show: false },
      axisLabel: { color: MUTED, fontSize: 10 },
    },
    yAxis: [
      { type:'value', name:'mm', nameTextStyle:{color:MUTED,fontSize:9}, splitLine:{lineStyle:{color:BORDER,type:'dashed'}}, axisLabel:{color:MUTED,fontSize:10} },
      { type:'value', name:'%',  nameTextStyle:{color:MUTED,fontSize:9}, min:0, max:100, axisLabel:{color:MUTED,fontSize:10}, splitLine:{show:false} },
    ],
    series: [
      {
        name: 'Rainfall mm', type: 'bar', yAxisIndex: 0, barMaxWidth: 16,
        data: MONTHLY_RAINFALL,
        itemStyle: { color: BLUE, borderRadius: [3,3,0,0] },
      },
      {
        name: 'Humidity %', type: 'line', yAxisIndex: 1, smooth: true, symbol: 'circle', symbolSize: 4,
        data: MONTHLY_HUMIDITY,
        lineStyle: { color: VIOLET, width: 2 }, itemStyle: { color: VIOLET },
      },
    ],
  });
  return chart;
}

/* ── 3. Max Temp Distribution ── */
function initTempDistChart() {
  const COLORS = [CYAN, BLUE, VIOLET, AMBER, '#f97316', ROSE];
  const chart = echarts.init(document.getElementById('tempDistChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP },
    grid: { top: 8, right: 8, bottom: 42, left: 34 },
    xAxis: {
      type: 'category', data: TEMP_DIST_LABELS,
      axisLine: { lineStyle: { color: BORDER } }, axisTick: { show: false },
      axisLabel: { color: MUTED, fontSize: 9, rotate: 18 },
    },
    yAxis: { type:'value', splitLine:{lineStyle:{color:BORDER,type:'dashed'}}, axisLabel:{color:MUTED,fontSize:10} },
    series: [{
      type: 'bar', barMaxWidth: 24,
      data: TEMP_DIST.map((v, i) => ({ value: v, itemStyle: { color: COLORS[i] } })),
      itemStyle: { borderRadius: [3,3,0,0] },
      label: { show: true, position: 'top', color: MUTED, fontSize: 9 },
    }],
  });
  return chart;
}

/* ── 4. Humidity Distribution ── */
function initHumDistChart() {
  const chart = echarts.init(document.getElementById('humDistChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP },
    grid: { top: 8, right: 8, bottom: 42, left: 34 },
    xAxis: {
      type: 'category', data: HUMIDITY_DIST_LABELS,
      axisLine: { lineStyle: { color: BORDER } }, axisTick: { show: false },
      axisLabel: { color: MUTED, fontSize: 9, rotate: 18 },
    },
    yAxis: { type:'value', splitLine:{lineStyle:{color:BORDER,type:'dashed'}}, axisLabel:{color:MUTED,fontSize:10} },
    series: [{
      type: 'bar', barMaxWidth: 32,
      data: HUMIDITY_DIST,
      itemStyle: { color: CYAN, borderRadius: [3,3,0,0] },
      label: { show: true, position: 'top', color: MUTED, fontSize: 9 },
    }],
  });
  return chart;
}

/* ── 5. Cloud Cover Distribution ── */
function initCloudChart() {
  const COLORS = [AMBER, BLUE, '#475569'];
  const chart = echarts.init(document.getElementById('cloudChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP },
    grid: { top: 8, right: 8, bottom: 28, left: 38 },
    xAxis: {
      type: 'category', data: CLOUD_DIST_LABELS,
      axisLine: { lineStyle: { color: BORDER } }, axisTick: { show: false },
      axisLabel: { color: MUTED, fontSize: 9 },
    },
    yAxis: {
      type: 'value', name: 'Days', nameTextStyle: { color: MUTED, fontSize: 9 },
      splitLine: { lineStyle: { color: BORDER, type: 'dashed' } }, axisLabel: { color: MUTED, fontSize: 10 },
    },
    series: [{
      type: 'bar', barMaxWidth: 48,
      data: CLOUD_DIST.map((v, i) => ({ value: v, itemStyle: { color: COLORS[i] } })),
      itemStyle: { borderRadius: [3,3,0,0] },
      label: { show: true, position: 'top', color: MUTED, fontSize: 10, formatter: '{c}' },
    }],
  });
  return chart;
}

/* ── 6. Wind Gust Direction ── */
function initWindChart() {
  const WIND_COLORS = [CYAN, CYAN, CYAN, BLUE, BLUE, BLUE, VIOLET, ROSE];
  const chart = echarts.init(document.getElementById('windChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP },
    grid: { top: 8, right: 18, bottom: 8, left: 8, containLabel: true },
    xAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: BORDER, type: 'dashed' } },
      axisLabel: { color: MUTED, fontSize: 10 },
    },
    yAxis: {
      type: 'category', data: WIND_DIRS,
      axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { color: MUTED, fontSize: 10 },
    },
    series: [{
      type: 'bar', barMaxWidth: 16,
      data: WIND_COUNTS,
      itemStyle: {
        color: (params) => WIND_COLORS[params.dataIndex],
        borderRadius: [0,3,3,0],
      },
      label: { show: true, position: 'right', color: MUTED, fontSize: 9 },
    }],
  });
  return chart;
}

/* ── 7. Rain Today vs Tomorrow (donut) ── */
function initRainPieChart() {
  const PIE_COLORS = [BLUE, '#1f2937', VIOLET, '#0e1117'];
  const chart = echarts.init(document.getElementById('rainPieChart'));
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { ...TOOLTIP },
    legend: { ...LEGEND, bottom: 0 },
    series: [{
      type: 'pie', radius: ['38%','65%'], center: ['50%','44%'],
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 11, color: TEXT, formatter: '{b}\n{c} days' } },
      data: RAIN_DATA.map((d, i) => ({ ...d, itemStyle: { color: PIE_COLORS[i] } })),
    }],
  });
  return chart;
}

/* ── Boot: initialise all charts & handle resize ── */
function initAllCharts() {
  const charts = [
    initTempChart(),
    initRainChart(),
    initTempDistChart(),
    initHumDistChart(),
    initCloudChart(),
    initWindChart(),
    initRainPieChart(),
  ];
  window.addEventListener('resize', () => charts.forEach(c => c.resize()));
}

document.addEventListener('DOMContentLoaded', initAllCharts);
