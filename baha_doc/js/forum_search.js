(function(e,i){function p(){var y,C,c=function(t){return decodeURIComponent((new RegExp("[?|&]"+t+"=([^&;]+?)(&|#|;|$)").exec(location.search)||[null,""])[1].replace(/\+/g,"%20"))||null},b=function(t){return Object.keys(t).map(function(s){return t[s]}).join(" ")},g=function(t,s){return"/search.php?bsn="+t+"&q="+encodeURIComponent(s)};const f="ckFORUM_searchType";this.initializeUI=function(){this.bsn=Number(c("bsn")),this.searchTerm={},this.searchTerm.bsn="more:pagemap:thread-bsn:"+this.bsn,this.searchTerm.filename="more:pagemap:thread-filename:C",this.searchBoxRender(),this.resetGoogleStyle(),this.saveRecentSearch(),this.keywordsRender(),google.search.cse.element.getElement("forumSearch").prefillQuery(c("q"));var t=c("qt"),s=c("q");if(t&&s||useOldSearch||Cookies.get(f)=="baha"){e("#searchbox").hide(),e("#searchbox_mobile").hide(),e("#old_search_searchbox").show(),e("#old_search_searchbox_mobile").show();var r;i.location.pathname=="/Bo.php"?(t==6?r="\u627E\u4F5C\u8005":t==7?r="\u627EM\u6587":r="\u627E\u6A19\u984C",e("#old_search_input").attr("placeholder","\u627E\u4F5C\u8005")):(r="\u627E\u6A19\u984C",e("#old_search_input").attr("placeholder","\u641C\u5C0B\u6B64\u54C8\u5566\u677F")),e("#old_search_input_mobile").attr("placeholder",r)}},this.searchBoxRender=function(){var t="https://forum.gamer.com.tw/search.php?bsn="+this.bsn;i.location.pathname=="/Bo.php"&&(t="Bo.php?bsn="+this.bsn+"&qt=6"),google.search.cse.element.render({div:"searchbox",attributes:{autoCompleteMaxCompletions:5,autoCompleteMatchType:"any",resultsUrl:t,queryParameterName:"q",gaCategoryParameter:this.bsn,gaQueryParameter:"q",enableHistory:!0},tag:"searchbox-only",gname:"forumSearch"})},this.searchResultsRender=function(t){google.search.cse.element.render({div:"searchresults",attributes:{webSearchQueryAddition:b(this.searchTerm),linkTarget:"_blank",queryParameterName:"q",gaCategoryParameter:this.bsn,gaQueryParameter:"q",filters:1,enableOrderBy:t},tag:"searchresults-only",gname:"forumSearch"})},this.searchResultsReload=function(t,s){e("#searchresults").empty(),this.searchResultsRender(t),s&&google.search.cse.element.getElement("forumSearch").execute(s)},this.resetGoogleStyle=function(){var t=e('link[href$="default.css"],link[href$="default+zh_TW.css"]');t.filter('[href*="www.google.com"]').remove();var s=e(".gcse-bar"),r=e("#gsc-i-id1"),a=e(".gcse-option-control"),o=e(".gcse-tab-child");s.on("mouseenter",function(){e(".gcse-option, .gsc-input-box").addClass("is-hover")}).on("mouseleave",function(){e(".gcse-dropdown").hasClass("is-active")||(e(".gcse-option, .gsc-input-box").removeClass("is-hover"),a.removeClass("is-active"))}),e("#old_search_input").on("focus",function(){e(".gcse-suggest").addClass("is-active")}).on("blur",function(){e(".gcse-dropdown:hover").length==0&&e(".gcse-dropdown").removeClass("is-active"),e(".gsc-input-box").removeClass("is-focus is-hover")}),e("#old_search_input_mobile").on("focus",function(){e(".gcse-suggest").addClass("is-active")}).on("blur",function(){e(".gcse-dropdown:hover").length==0&&e(".gcse-dropdown").removeClass("is-active"),e(".gsc-input-box").removeClass("is-focus is-hover")}),r.on("focus",function(){e(".gcse-suggest").addClass("is-active")}).on("blur",function(){e(".gcse-dropdown:hover").length===0&&e(".gcse-dropdown").removeClass("is-active"),e(".gsc-input-box").removeClass("is-focus is-hover")}).on("mouseenter",function(){e(this).is(":focus")&&!e(".gcse-suggest").hasClass("is-active")&&e(".gcse-suggest").addClass("is-active")}).attr("placeholder","\u641C\u5C0B\u6B64\u54C8\u5566\u677F"),e("input.gsc-input").on("focus",function(){e(".gsc-input-box, .gcse-option").addClass("is-focus")}).on("blur",function(){e(".gsc-input-box").removeClass("is-focus")}),a.on("click",function(){e(this).hasClass("is-active")?e(this).blur():(e(".gcse-sort").addClass("is-active"),e(this).addClass("is-active").focus(),e(".gcse-suggest").removeClass("is-active"))}).on("blur",function(){a.removeClass("is-active"),e(".gcse-dropdown:hover").length===0&&e(".gcse-dropdown").removeClass("is-active")}),e(".gcse-sort > ul > li").on("click",function(){e(".gcse-sort").removeClass("is-active");var n=e(".gcse-dropdown > ul > li").index(e(this));if(n>4&&(n=n-4),n==3)Cookies.set(f,"google",{expires:365}),e("#old_search_searchbox").hide(),e("#old_search_searchbox_mobile").hide(),e("#gsc-i-id1").val(e("#old_search_input").val()),e("#searchbox").show(),e("#searchbox_mobile").show(),e("#gsc-i-id1").focus();else switch(Cookies.set(f,"baha",{expires:365}),e("#searchbox").hide(),e("#old_search_input").val(e("#gsc-i-id1").val()),e("#old_search_searchbox").show(),e("#old_search_input").attr("placeholder",e(this).find(".gcse-sort-title").text()).focus(),e("#searchbox_mobile").hide(),e("#old_search_input_mobile").val(e("#gsc-i-id1").val()),e("#old_search_searchbox_mobile").show(),e("#old_search_input_mobile").attr("placeholder",e(this).find(".gcse-sort-title").text()).focus(),n){case 1:e("#stype").val(2),e("#stype_mobile").val(2);break;case 2:e("#stype").val(4),e("#stype_mobile").val(4);break;default:e("#stype").val(1),e("#stype_mobile").val(1);break}});var h=e(".gcse-clear"),l=this;h.click(function(){location.href="/B.php?bsn="+l.bsn}),c("qt")&&c("q")?h.show():h.hide(),e("#gsc-i-id1").keyup(function(n){e(this).val().length>0?e(".gcse-option-control, .gcse-suggest").removeClass("is-active"):e(".gcse-suggest").addClass("is-active")}),e("#old_search_form").submit(function(){if(e("#old_search_input").val().length<1)return Dialogify.alert("\u8ACB\u8F38\u5165\u641C\u5C0B\u5167\u5BB9"),!1}),e("#old_search_form_mobile").submit(function(){if(e("#old_search_input_mobile").val().length<1)return Dialogify.alert("\u8ACB\u8F38\u5165\u641C\u5C0B\u5167\u5BB9"),!1});var u=this;o.on("click",function(){o.removeClass("is-active"),e(this).addClass("is-active"),u.changeArea(e(this).attr("id"))})},this.saveRecentSearch=function(){var t=c("q");if(t&&typeof Storage<"u"){var s=JSON.parse(localStorage.getItem("forumSearch"));s=s||{},s[this.bsn]=s[this.bsn]?s[this.bsn]:[],s[this.bsn].unshift(t),s[this.bsn]=s[this.bsn].filter(function(r,a,o){return o.indexOf(r)==a}),s[this.bsn]=s[this.bsn].slice(0,15),localStorage.setItem("forumSearch",JSON.stringify(s))}},this.keywordsRender=function(){var t=[];if(typeof Storage<"u"){var s=JSON.parse(localStorage.getItem("forumSearch"));s!=null&&s[this.bsn]!=null&&Array.isArray(s[this.bsn])&&(t=s[this.bsn].map(function(a){var o={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"};return a.replace(/[&<>"']/g,function(h){return o[h]})}))}!hotKeywords.length&&!t.length?e(".search-suggest, .gcse-suggest").hide():(r("\u6700\u8FD1\u641C\u5C0B",t,"search-suggest-tag search-suggest-tag_recent",e(".right-child"),this.bsn,!0,'data-gtm-click="\u9EDE\u64CA\u6700\u8FD1\u641C\u5C0B" data-gtm-service="forum" data-gtm-page="\u641C\u5C0B\u7D50\u679C\u9801"'),r("\u6700\u8FD1\u641C\u5C0B",t,"gcse-suggest-tag",e("#gcse-suggest-child-recently_mobile"),this.bsn),r("\u6700\u8FD1\u641C\u5C0B",t,"gcse-suggest-tag",e("#gcse-suggest-child-recently"),this.bsn,!0),r("\u71B1\u9580\u641C\u5C0B",hotKeywords,"search-suggest-tag",e(".right-child"),this.bsn,!1,'data-gtm-click="\u9EDE\u64CA\u71B1\u9580\u641C\u5C0B" data-gtm-service="forum" data-gtm-page="\u641C\u5C0B\u7D50\u679C\u9801"'),r("\u71B1\u9580\u641C\u5C0B",hotKeywords,"gcse-suggest-tag",e("#gcse-suggest-child-hot"),this.bsn),r("\u71B1\u9580\u641C\u5C0B",hotKeywords,"gcse-suggest-tag",e("#gcse-suggest-child-hot_mobile"),this.bsn),e("a[data-search-dynamic]").bind("click",function(){var a;e(this).parent().hasClass("gcse-suggest-tag")?e("#searchbox").is(":visible")?a="search.php?bsn="+e(this).data("bsn")+"&q="+e(this).text():e("#stype").val()==2?a="search.php?bsn="+e('input[name="bsn"]').val()+"&author="+e(this).text():e("#stype").val()==4?a="search.php?bsn="+e('input[name="bsn"]').val()+"&type=m&q="+e(this).text():a=g(e(this).data("bsn"),e(this).text()):i.location.pathname=="/search.php"?a="search.php?bsn="+e(this).data("bsn")+"&q="+e(this).text():e("#stype").val()==2?a="search.php?bsn="+e('input[name="bsn"]').val()+"&author="+e(this).text():e("#stype").val()==4?a="search.php?bsn="+e('input[name="bsn"]').val()+"&type=m&q="+e(this).text():a=g(e(this).data("bsn"),e(this).text()),i.location.pathname=="/Bo.php"&&/^[a-zA-Z][a-zA-Z0-9]{1,11}$/.test(e(this).text().trim())&&(a="Bo.php?bsn="+e('input[name="bsn"]').val()+"&qt=6&q="+encodeURIComponent(e(this).text().trim())),e(this).attr("href",a)}),t.length||e("#gcse-suggest-child-recently").remove(),hotKeywords.length||e("#gcse-suggest-child-hot").remove());function r(a,o,h,l,u,n=!1,v=""){if(o.length){var d=e("<div>").addClass(h);for(var _ in o)d.append('<a data-bsn="'+u+'" '+v+" data-search-dynamic>"+o[_]+"</a>");let m="<h3>"+a;n?m+='<a href="javascript:forumSearch.removeKeyword('+u+');" class="clean"><i class="fa fa-trash"></i></a></h3>':m+="</h3>",l.append(m),l.append(d)}}},this.removeKeyword=function(t){if(typeof Storage<"u"){var s=JSON.parse(localStorage.getItem("forumSearch"));delete s[t],localStorage.setItem("forumSearch",JSON.stringify(s)),e("#gcse-suggest-child-recently").remove(),e(".search-suggest-tag_recent").prev().remove(),e(".search-suggest-tag_recent").empty()}},this.changeCondition=function(){this.searchTerm.bsn="more:pagemap:thread-bsn:"+this.bsn,this.searchTerm.filename="more:pagemap:thread-filename:C",this.searchTerm.subbsn=e("#filter-subbsn").val()?"more:pagemap:thread-subbsn:"+e("#filter-subbsn").val():"",this.searchTerm.type="",e("#filter-article").is(":checked")&&(this.searchTerm.type="more:pagemap:thread-extract:T"),e("#filter-author").is(":checked")&&(this.searchTerm.type="more:pagemap:thread-author:"+e("#gsc-i-id1").val(),this.searchTerm.filename="more:pagemap:thread-filename:Co"),this.searchResultsReload(!0)},this.changeArea=function(t){var s=c("q");switch(this.searchTerm={},t){case"area_board":e(".gcse-forum").hide(),this.searchTerm.filename="more:pagemap:thread-filename:A",s&&this.searchResultsReload(!1,s);break;case"area_others":e(".gcse-forum").hide(),s&&this.searchResultsReload(!1,s+" "+e(".BH-menuE li:nth-child(2)").text()+" -site:forum.gamer.com.tw");break;case"area_extract":e(".gcse-forum").hide(),this.searchTerm.bsn="more:pagemap:thread-bsn:"+this.bsn,this.searchTerm.filename="more:pagemap:thread-filename:G2",s&&this.searchResultsReload(!0,s);break;default:e(".gcse-forum").show(),this.searchTerm.bsn="more:pagemap:thread-bsn:"+this.bsn,this.searchTerm.filename="more:pagemap:thread-filename:C",s&&this.searchResultsReload(!0,s);break}},this.submit=function(){var t=e("#old_search_input").val();if(jQuery("#old_search_input_mobile").is(":visible")&&(t=e("#old_search_input_mobile").val()),i.location.pathname=="/Bo.php")return i.location.href="Bo.php?bsn="+this.bsn+"&qt=6&q="+encodeURIComponent(t),!1;switch(e("#stype").val()){case"2":i.location.href="search.php?bsn="+this.bsn+"&author="+encodeURIComponent(t);break;case"4":i.location.href="search.php?bsn="+this.bsn+"&type=m&q="+encodeURIComponent(t);break;default:i.location.href=g(this.bsn,t)}return!1}}i.forumSearch=new p})(jQuery,window),window.__gcse={parsetags:"explicit",callback:function(){document.readyState=="complete"?forumSearch.initializeUI():google.setOnLoadCallback(function(){forumSearch.initializeUI()},!0)}};