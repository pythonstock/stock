<template>
  <div class="dashboard-container">

<div class="clearfix">
		<div class="pull-left tableTools-container">
			<h3>基础库版本</h3>
			<p>1，pandas使用【 {{ pandasVersion }} 】版本， <el-link type="primary" href="https://www.runoob.com/pandas/pandas-tutorial.html" target="_blank">中文文档</el-link> </p>
			<p>2，numpy使用【 {{ numpyVersion }} 】版本， <el-link type="primary" href="https://www.runoob.com/numpy/numpy-tutorial.html" target="_blank">中文文档</el-link></p>
			<p>3，sqlalchemy使用【 {{ sqlalchemyVersion }} 】版本， <el-link type="primary" href="https://docs.sqlalchemy.org/en/20/" target="_blank">英文文档</el-link></p>
			<p>4，akshare使用【 {{ akshareVersion }} 】版本， <el-link type="primary" href="https://akshare.akfamily.xyz/data/index/index.html" target="_blank">中文文档</el-link></p>
			<p>5，bokeh使用【 {{ bokehVersion }} 】版本， <el-link type="primary" href="http://docs.bokeh.org/en/latest/" target="_blank">官方文档</el-link></p>
			<p>6，stockstats使用【 {{ stockstatsVersion }} 】版本， <el-link type="primary" href="https://github.com/jealous/stockstats/" target="_blank">官方文档</el-link></p>
		</div>
	</div>

	<div class="clearfix">
		<div class="pull-left tableTools-container">
			<h3>相关资料信息</h3>
			<p>1，github项目地址。<el-link type="primary" href="https://gitee.com/pythonstock/stock" target="_blank">pythonstock</el-link></p>
			<p>2，博客地址。<el-link type="primary" href="https://blog.csdn.net/freewebsys/category_9285317.html" target="_blank">博客地址</el-link></p>
		</div>
	</div>

	<div class="clearfix">
		<div class="pull-left tableTools-container">
			<h3>2021年9月20日更新，发布2.0版本</h3>
			<p>1，修复bokeh的版本升级问题，可以显示趋势数据了。</p>
			<p>2，使用 stock_zh_ah_name 做每日数据。</p>
			<p>3，AkShare 升级到 1.1.9 版本。</p>
		</div>
	</div>

	<div class="clearfix">
		<div class="pull-left tableTools-container">
			<h3>2021年8月31日更新job服务</h3>
			<p>1，过滤包括：600，6006，601，000，001，002，且不包括ST的股票数据。。</p>
			<p>2，使用 stock_zh_ah_name 做每日数据。</p>
			<p>3，AkShare 升级到 1.0.80 版本。</p>

		</div>
	</div>

	<div class="clearfix">
		<div class="pull-left tableTools-container">
			<h3>2021年6月3日使用 AkShare 做数据抓取服务</h3>
			<p>1，使用 stock_zh_a_spot 做实时行情数据。</p>
			<p>2，使用 stock_zh_a_daily 做历史数据统计。</p>
			<p>3，升级基础镜像使用python3.7，AkShare 的 0.9.65 版本。</p>
		</div>
	</div>



  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { fetchPackageVersion } from '@/api/package'

export default {
  name: '首页',
  data() {
    return {
			pandasVersion: '',
			numpyVersion: '',
			sqlalchemyVersion: '',
			akshareVersion: '',
			bokehVersion: '',
			stockstatsVersion: '',
	}
  },
  created() {
    this.getPackageVersion()
  },
  methods: {
    getPackageVersion() {
	console.info("$router.params : ", this.$router.params)
      fetchPackageVersion().then(response => {

		this.pandasVersion = response.pandasVersion
		this.numpyVersion = response.numpyVersion
		this.sqlalchemyVersion = response.sqlalchemyVersion
		this.akshareVersion = response.akshareVersion
		this.bokehVersion = response.bokehVersion
		this.stockstatsVersion = response.stockstatsVersion

      })
	}
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>