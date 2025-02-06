(function(r,o){"use strict";function f(t,e,i){if(User.Login.isLogin()){s(t,e,i);return}User.Login.requireLoginIframe(function(){if(User.Login.getUserid().toLowerCase()!=t.toLowerCase()){s(t,e,function(){location.reload()});return}location.reload()})}function s(t,e,i){Util.Api.call("POST","https://wall.gamer.com.tw/app/v1/friend_cancel.php",{userId:t,class:e},!0,!1).done(function(a){if(a.code==0)return Dialogify.alert(a.message),!1;i()})}let p={userFollowFinish:t=>{let e=o(".article_gamercard .gamecard__follow");t==1?e.addClass("is-active").text("\u5DF2\u8FFD\u8E64"):e.removeClass("is-active").text("\u8FFD\u8E64")},applyDarenSpecialty:(t,e,i)=>{Dialogify.confirm("\u662F\u5426\u78BA\u8A8D\u7533\u8ACB"+e+"\u5C08\u7CBE",{ok:function(){Util.Api.call("POST","https://api.gamer.com.tw/creator/v1/daren_specialty_apply.php",{specialty:t},!0,!1).done(function(a){if(typeof a.error<"u")return Util.errorHandler()(a.error);i!=null&&i!=null?i.call(a):Dialogify.alert("\u7533\u8ACB\u6210\u529F",{close:function(){location.reload()}})})},cancel:function(){this.close()}})},applyDaren:t=>{let e=nunjucks.render("daren_apply.njk.html",{});new Dialogify(e,{size:Dialogify.SIZE_LARGE}).title("\u7533\u8ACB\u9054\u4EBA").buttons(['<div class="check-group text-left"><input id="daren-agree" type="checkbox"><label for="daren-agree"><div class="label-icon"><i class="fa fa-check"></i></div><h6>\u6211\u5DF2\u95B1\u8B80\u4E14\u540C\u610F<a href="https://forum.gamer.com.tw/Co.php?bsn=60404&sn=102059" target="_blank">\u7533\u8ACB\u898F\u7BC4</a></h6></label></div>',{text:"\u53D6\u6D88",click:function(){this.close()}},{text:"\u9001\u51FA",type:Dialogify.BUTTON_PRIMARY,click:function(i){if(!o("#daren-agree").prop("checked")){Dialogify.alert("\u8ACB\u52FE\u9078\u5DF2\u95B1\u8B80\u4E14\u540C\u610F\u9054\u4EBA\u7533\u8ACB\u898F\u7BC4"),i.preventDefault();return}Util.Api.call("POST","https://api.gamer.com.tw/creator/v1/daren_apply.php",{},!0,!1).done(function(a){if(typeof a.error<"u")return Util.errorHandler()(a.error);t!=null&&t!=null?t.call(a):Dialogify.alert("\u7533\u8ACB\u6210\u529F",{close:function(){location.reload()}})}),this.close()}}]).showModal()},applyDarenUpgrade:t=>{Dialogify.confirm("\u662F\u5426\u78BA\u8A8D\u7533\u8ACB\u9054\u4EBA\u5347\u7D1A\uFF1F",{ok:function(){Util.Api.call("POST","https://api.gamer.com.tw/creator/v1/daren_apply_upgrade.php",{},!0,!1).done(function(e){if(typeof e.error<"u")return Util.errorHandler()(e.error);t!=null&&t!=null?t.call(e):Dialogify.alert("\u7533\u8ACB\u6210\u529F",{close:function(){location.reload()}})})},cancel:function(){this.close()}})},darencard:function(){let t=o(".article_gamercard");t.length!=0&&o(".gamecard__background, .gamecard__game",t).click(function(e){let i=o(e.target),a;if(i.hasClass("article_gamercard")?a=i:a=i.parents(".article_gamercard"),i.hasClass("gamecard__follow")){let l=i.hasClass("is-active")?2:1;new Util.Ga4.GtmParams().service("home").click(l==2?"\u9EDE\u64CA\u9000\u8FFD\u8E64\u52C7\u8005":"\u9EDE\u64CA\u8FFD\u8E64\u52C7\u8005").page("C\u9801").area("\u9054\u4EBA\u5361\u7247").pushDataLayer(),!User.Login.isLogin()&&typeof BahamutJs<"u"&&BahamutJs.userFollow!="undefined"?BahamutJs.userFollow(a.data("userid"),l):f(a.data("userid"),l,function(){Bahamut.Creator.userFollowFinish(l)})}else i.filter('[data-daren="title"]').length?new Util.Ga4.GtmParams().service("home").click("\u9EDE\u64CA\u4E86\u89E3\u9054\u4EBA").page("C\u9801").area("\u9054\u4EBA\u5361\u7247").pushDataLayer():(new Util.Ga4.GtmParams().service("home").click("\u9EDE\u64CA\u5C0F\u5C4B").page("C\u9801").area("\u9054\u4EBA\u5361\u7247").pushDataLayer(),typeof BahamutJs<"u"?r.location.href="https://home.gamer.com.tw/"+a.data("userid"):r.open("https://home.gamer.com.tw/"+a.data("userid")))})},getHonorData:function(t,e){if(typeof r.honorData!="function")return{img:`https://p2.bahamut.com.tw/HOME/honor/${t}.gif`,title:"",link:""};const i=r.honorData();return i[t]?{img:`https://p2.bahamut.com.tw/HOME/honor/${t}.gif${i[t][2]}`,title:i[t][0],link:i[t][1]==1?`https://avatar1.gamer.com.tw/switchhonor.php?uid=${e}&htype=${t}`:""}:{img:"",title:"",link:""}},checkDarenContinue:function(t){Util.Api.call("POST","https://api.gamer.com.tw/creator/v1/daren_check_continue.php",{},!1,!1).done(function(e){if(typeof e.error<"u")return Util.errorHandler()(e.error);if(t!=null&&t!=null)t.call(e);else{var i=e.data.darenContinue?"":'style="color:#F44336;"',a=`
                        <style>.perm_icon:before {font: normal normal normal 14px/1 FontAwesome}</style>
                        <style>.perm_icon {padding-top: 5px; margin-right:5px; margin-top: 5px;}</style>
                        <style>.perm_pass:before {content: "\\f05d"; color: green;}</style>
                        <style>.perm_fail:before {content: "\\f05c"; color: red;}</style>
                        <div class="applydaren">
                            <div class="dialog__content-list">
                                <h5 class="dialog__content-title"> \u5275\u4F5C\u8EAB\u5206\uFF1A </h5>
                                <div class="dialog__content-text">
                                    <b>${e.data.title}</b>
                                </div>
                            </div>
                            <div class="dialog__content-list">
                                <h5 class="dialog__content-title"> \u7E8C\u4EFB\u9032\u5EA6\uFF1A </h5>
                                <div class="dialog__content-text">
                                    <b ${i}>${e.data.darenContinueText}</b><small>${e.data.extraContinueText}</small>
                                </div>
                            </div>
                            <div class="dialog__content-list">
                                <h5 class="dialog__content-title" style="margin-bottom: 5px;"> \u7E8C\u4EFB\u689D\u4EF6 </h5>

                    `;let l='<i class="perm_icon perm_pass"></i>',d='<i class="perm_icon perm_fail"></i>';Object.keys(e.data.condition).forEach(n=>{var c=e.data.condition[n].eligible==!0?l:d;a+=`<p>${c}${n}\uFF1A${e.data.condition[n].text}</p>`}),a+="</div>",e.data.extraCondition!=""&&(a+=`<div class="dialog__content-list">
                                        <h5 class="dialog__content-title"> \u7E8C\u4EFB\u689D\u4EF6 2 </h5>
                                    `,Object.keys(e.data.extraCondition).forEach(n=>{var c=e.data.extraCondition[n].eligible==!0?l:d;a+=`<p>${c}${n}\uFF1A${e.data.extraCondition[n].text}</p>`}),a+="</div>"),a+"",new Dialogify(a,{size:Dialogify.SIZE_LARGE}).title(`${e.data.userid} \u5275\u4F5C\u8EAB\u5206\u7E8C\u4EFB\u9032\u5EA6`).showModal()}})}};r.Bahamut=r.Bahamut||{},r.Bahamut.Creator=p})(window,jQuery);