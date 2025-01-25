document.addEventListener('DOMContentLoaded',async()=>{
    let apiService = new ApiService(BASEURL)
    let dados = await apiService.getAll('report_iscas')
    popula_tbody_paginacao('paginacao','tbodyIscas',dados,{},1,999,false)
})