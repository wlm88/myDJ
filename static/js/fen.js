var theUL = document.getElementById("pageListTableBody");
var totalPage = document.getElementById("spanTotalPage");
var pageNum = document.getElementById("spanPageNum"); //获取当前页<span>
var spanPre = document.getElementById("spanPre"); //获取上一页<span>
var spanNext = document.getElementById("spanNext"); //获取下一页<span>
var spanFirst = document.getElementById("spanFirst"); //获取第一页<span>
var spanLast = document.getElementById("spanLast"); //获取最后一页<span>
var numberRowsInTable = theUL.getElementsByTagName("tr").length; //记录总条数
var pageSize = 20; //每页显示的记录条数
var page = 1; //当前页，默认第一页

//下一页
function next(){
    hideTable();
    currentRow = pageSize * page;
    maxRow = currentRow + pageSize;
    if ( maxRow > numberRowsInTable ) maxRow = numberRowsInTable;
    for ( var i = currentRow; i< maxRow; i++ ){
        theUL.getElementsByTagName("tr")[i].style.display = '';
    }
    page++;
    if ( maxRow == numberRowsInTable ) {
        nextText();
        lastText();
    }
    showPage();
    preLink();
    firstLink();
}

//上一页
function pre(){
    hideTable();
    page--;
    currentRow = pageSize * page;
    maxRow = currentRow - pageSize;
    if ( currentRow > numberRowsInTable ) currentRow = numberRowsInTable;
    for ( var i = maxRow; i< currentRow; i++ ){
        theUL.getElementsByTagName("tr")[i].style.display = '';
    }
    if ( maxRow == 0 ){
        preText();
        firstText();
    }
    showPage();
    nextLink();
    lastLink();
}

//第一页
function first(){
    hideTable();
    page = 1;
    for ( var i = 0; i<pageSize; i++ ){
        theUL.getElementsByTagName("tr")[i].style.display = '';
    }
    showPage();
    firstText();
    preText();
    nextLink();
    lastLink();
}

//最后一页
function last(){
    hideTable();
    page = pageCount();
    currentRow = pageSize * (page - 1);
    for ( var i = currentRow; i<numberRowsInTable; i++ ){
        theUL.getElementsByTagName("tr")[i].style.display = '';
    }
    showPage();
    preLink();
    nextText();
    firstLink();
    lastText();
}

function hideTable(){
    for ( var i = 0; i<numberRowsInTable; i++ ){
        theUL.getElementsByTagName("tr")[i].style.display = 'none';
    }
}

function showPage(){
    pageNum.innerHTML = page;
}

//总共页数
function pageCount(){
    return Math.ceil(numberRowsInTable/pageSize);
}
//显示链接
function preLink(){
    spanPre.innerHTML = "<a href='javascript:pre();'>上一页</a>";
}
function preText(){
    spanPre.innerHTML = "上一页";
}
function nextLink(){
    spanNext.innerHTML = "<a href='javascript:next();'>下一页</a>";
}
function nextText(){
    spanNext.innerHTML = "下一页";
}
function firstLink(){
    spanFirst.innerHTML = "<a href='javascript:first();'>首页</a>";
}
function firstText(){
    spanFirst.innerHTML = "首页";
}
function lastLink(){
    spanLast.innerHTML = "<a href='javascript:last();'>末页</a>";
}
function lastText(){
    spanLast.innerHTML = "末页";
}

//隐藏
function hide(){
    for ( var i = pageSize; i<numberRowsInTable; i++ ){
        theUL.getElementsByTagName("tr")[i].style.display = 'none';
    }
    totalPage.innerHTML = pageCount();
    pageNum.innerHTML = '1';
    nextLink();
    lastLink();
}
hide();
