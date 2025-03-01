import request from '@/utils/request'

export function fetchPackageVersion(query) {
  return request({
    url: '/api/v1/package_verison',
    method: 'get',
    params: query
  })
}

