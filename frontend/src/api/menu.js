import request from '@/utils/request'

// 同步获得菜单相关数据。

export  function fetchMenuList(query) {
  return request({
    url: '/api/v1/menu_list',
    method: 'get',
    params: query
  })
}

