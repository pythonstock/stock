<template>
  <div class="app-container">

    <div class="filter-container">
      <el-date-picker
      v-model="queryDate" type="date"  format="yyyyMMdd"
                value-format="yyyyMMdd"
      placeholder="选择日期">

    </el-date-picker>
      <el-input v-model="queryCode" placeholder="code" 
      style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
     
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
 
    </div>

    <el-table :key="tableKey" v-loading="listLoading" :data="list"
      stripe border fit fixed highlight-current-row style="width: 100%;" 
      @sort-change="sortChange"
    >

      <!-- 
        columns=['date','code','name','latest_price','quote_change','ups_downs','volume','turnover',
                 'amplitude','high','low','open','closed','quantity_ratio','turnover_rate','pe_dynamic','pb'],
        column_names=['日期','代码','名称','最新价','涨跌幅','涨跌额','成交量','成交额',
                      '振幅','最高','最低','今开','昨收','量比','换手率','动态市盈率','市净率'],
        -->

        <el-table-column sortable v-for="column in tableColumns" :key="column.column" 
          :label="column.columnName" :prop="column.column" align="center" width="120"/>


      <el-table-column  fixed="right" label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleView(row,$index)">
            查看
          </el-button>
          <!-- <el-button v-if="row.code!='published'" size="mini" type="success" @click="handleModifyStatus(row,'published')">
            Publish
          </el-button> -->

        </template>
      </el-table-column>

    </el-table>

    <!--
    https://element.eleme.cn/#/zh-CN/component/pagination#slot
    文档设置分页数据：
    -->
    <pagination v-show="total>0" :total="total" 
      :page-sizes="[10, 20, 50, 100, 200, 300]"
      :page.sync="listQuery.page" :limit.sync="listQuery.limit" 
      @pagination="getList"/>

     
  </div>
</template>

<script>
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: [],
      tableColumns: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        importance: undefined,
        date: undefined,
        code: undefined,
        name: '',
        sort: '+id'
      },
      calendarTypeOptions,

      dialogFormVisible: false,
 
      queryDate: '',
      queryCode: ''

    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {

      console.info("$router.path:", this.$route.path)
      let table_name = this.$route.path.replace("/stock/table/","")
      console.info(table_name == ':tableName')
      if(table_name == ':tableName'){
        this.list=[]
        this.total=0
        this.listLoading = false
        return
      }
      console.info("$table_name:", table_name)
      this.listQuery.name =  table_name

      this.listQuery.date =  this.queryDate//this.$formatDate(this.queryDate, 'yyyyMMdd')
      this.listQuery.code =  this.queryCode
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        this.list = response.data
        this.tableColumns = response.tableColumns
        this.total = response.total
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    handleView(row, index) {
      this.$notify({
        title: 'Success',
        message: 'Delete Successfully'+row['code'],
        type: 'success',
        duration: 2000
      })
      //http://quote.eastmoney.com/%s.html
      const url = 'http://quote.eastmoney.com/'+row['code']+'.html'
      window.open(url, '_blank')
      this.list.splice(index, 1)
    },

    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
