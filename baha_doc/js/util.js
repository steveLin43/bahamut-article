(function ($, window, undefined) {
    'use strict';

    var UtilString = {
        utf8Length: function (str) {
            return new Blob([str]).size;
        },
        utf8Cut(str, utf8LengthLimit) {
            let origLength = UtilString.utf8Length(str);
            if (origLength <= utf8LengthLimit) {
                return str;
            }

            let result = '';
            for (let i = 1; i <= str.length; i++) {
                let tmp = str.slice(0, i);
                if (this.utf8Length(tmp) > utf8LengthLimit) {
                    break;
                }
                result = tmp;
            }

            return result;
        }
    }

    var UtilNumber = {
        format: function (num, glue) {
            if (isNaN(num)) {
                return NaN;
            }

            var n = '';
            if (num < 0) {
                num = Math.abs(num);
                n = '-';
            }

            var glue = (typeof glue === 'string') ? glue : ',';
            var digits = num.toString().split('.');

            var integerDigits = digits[0].split('');
            var threeDigits = [];

            while (integerDigits.length > 3) {
                threeDigits.unshift(integerDigits.splice(integerDigits.length - 3, 3).join(''));
            }

            threeDigits.unshift(integerDigits.join(''));
            digits[0] = threeDigits.join(glue);

            return n + digits.join('.');
        }
    }

    let UtilHtml = {
        encode: function (text) {
            let map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        },

        decode: function (html) {
            let map = {
                '&amp;': '&',
                '&lt;': '<',
                '&gt;': '>',
                '&quot;': '"',
                '&#039;': "'",
                '&#39;': "'"
            };
            return html.replace(/&(?:amp|lt|gt|quot|#0?39);/g, m => map[m]);
        }
    }
    let UtilApi = {
        call: function (method, url, data, csrf, hasFile) {
            let settings = {
                xhrFields: {
                    withCredentials: true
                },
                method: method
            };

            if (csrf) {
                let csrf = new Bahamut.Csrf();
                csrf.setCookie();
                settings['headers'] = csrf.getJqueryHeaders();
            }

            if (!url.match('^https://')) {
                url = 'https://api.gamer.com.tw/' + url;
            }

            settings.url = url;
            settings.data = data;

            if (hasFile) {
                settings.processData = false;
                settings.contentType = false;
            }

            return $.ajax(settings);
        }
    }

    let UtilUserAgent = {
        isMobile: function () {
            let ua = navigator.userAgent || navigator.vendor || window.opera;
            if (/android.+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(ua) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-/i.test(ua.substr(0, 4))) {
                return true;
            } else {
                return false;
            }
        }
    }

    //��蝣澆��隞�
    let UtilPagination = {
        showPageButton: function (container, currentPage, totalPage) {
            if (totalPage == 0) {
                $(container).html('');
                return;
            }

            let maxPageToShow = 5;
            let frontMax = 4;
            let extendPage = (maxPageToShow - 1)/2;
            let backMax = extendPage + 1;

            let start = 1;
            let end = totalPage;
            if (totalPage > 5) {
                if (currentPage <= 3) {
                    end = Math.min(Math.max(currentPage + extendPage, frontMax), totalPage);
                } else if ((totalPage - currentPage) >= 3) {
                    start = currentPage - extendPage;
                    end = currentPage + extendPage;
                } else {
                    start = Math.max(1, Math.min(currentPage - extendPage, totalPage - backMax));
                }
            }

            nunjucks.configure({ autoescape: true });
            let list = nunjucks.render('pagination.njk.html', {
                currentPage: currentPage,
                totalPage: totalPage,
                start: start,
                end: end+1
            });
            $(container).html(list);
            $('[name="common_pagination"]').off('click');
            $('[name="common_pagination"]').on('click', function() {
                let page = $(this).data('page');
                Util.Pagination.changePage(page);
            })
        },

        setCallback: function (callback) {
            this.callback = callback;
        },

        changePage: function (pageIndex) {
            if (typeof Util.Pagination.callback !== 'undefined') {
                Util.Pagination.callback(pageIndex);
                return;
            }

            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);

            window.scroll(0, 0);

            urlParams.set('page', pageIndex);
            history.replaceState('', '', '?'+urlParams.toString());
            location.reload();
        }
    }

    class AbstractTheme {
        static COOKIE_NAME = 'ckTheme';

        constructor() {
            if (this.constructor == AbstractTheme) {
                throw new Error('Abstract classes can not be instantiated.');
            }
        }

        static toggle() {
            const theme = new this;
            if (theme.getName() == theme.getCurrentThemeName()) {
                theme.remove();
            } else {
                theme.apply();
            }
        }

        static applying() {
            const theme = new this;
            return theme.getName() == theme.getCurrentThemeName();
        }

        apply() {
            window.document.querySelector('html').dataset.theme = this.getName();
            Cookies.set(AbstractTheme.COOKIE_NAME, this.getName(), { expires: 365, domain: 'gamer.com.tw' })
        }

        remove() {
            delete window.document.querySelector('html').dataset.theme;
            Cookies.remove(AbstractTheme.COOKIE_NAME, { domain: 'gamer.com.tw' });
        }

        getName() {
            throw new Error('Not implemented.');
        }

        getCurrentThemeName() {
            return window.document.querySelector('html').dataset?.theme ||
                Cookies.get(AbstractTheme.COOKIE_NAME);
        }
    }

    let UtilTheme = {
        Dark: class ThemeDark extends AbstractTheme {
            static bindSystemThemeChange(apply) {
                const darkTheme = new this;
                const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
                if (apply && mediaQuery.matches && darkTheme.getCurrentThemeName() != darkTheme.getName()) {
                    darkTheme.apply();
                }

                mediaQuery.addEventListener('change', e => {
                    if (e.matches) {
                        darkTheme.apply();
                    } else {
                        darkTheme.remove();
                    }
                });
            }

            apply() {
                super.apply();
                window.location.reload();
            }

            remove() {
                super.remove();
                window.location.reload();
            }

            getName() {
                return 'dark';
            }
        }
    };

    let Util = window.Util || {};

    Util.errorHandler = function (handler) {
        var d = {
            401: function () {
                window.User.Login.requireLogin();
            },
        };

        return function (err) {
            if (handler && handler[err.code]) {
                handler[err.code](err);
            } else if (d[err.code]) {
                d[err.code](err);
            } else {
                Dialogify.alert(err.message);
            }
        }
    }

    var UtilGa4 = {
        GtmParams: class GtmParams {
            static PREFIX = 'data-gtm-';

            #event;
            #params;

            constructor(params, event) {
                if (Array.isArray(params)) {
                    params = new Map(params);
                }

                this.#params = params || new Map();
                this.#event = event || 'all_click';
            }

            set(name, value) {
                if (!name || !value) {
                    return this;
                }

                switch (name) {
                    case GtmParams.PREFIX + 'click':
                        this.#params.delete(GtmParams.PREFIX + 'link-click');
                        break;
                    case GtmParams.PREFIX + 'link-click':
                        this.#params.delete(GtmParams.PREFIX + 'click');
                        break;
                    default:
                }

                this.#params.set(name, value);
                return this;
            }

            event(event) {
                this.#event = event;
                return this;
            }

            toHtmlAttr(leadingSpace) {
                let attrs = [];
                for (let [name, value] of this.#params) {
                    name = name.replaceAll(' ', '-');
                    value = value.replaceAll('"', '&quot;');
                    attrs.push(`${name}="${value}"`);
                }

                let attrsString = attrs.join(' ');
                if (leadingSpace) {
                    attrsString = ' ' + attrsString;
                }

                return attrsString;
            }

            setElementAttr(elem) {
                for (let [name, value] of this.#params) {
                    name = name.replaceAll(' ', '-');
                    value = value.replaceAll('"', '&quot;');
                    elem.setAttribute(name, value);
                }
            }

            pushDataLayer() {
                let dataLayer = {};
                dataLayer['event'] = this.#event;
                for (let [name, value] of this.#params) {
                    name = name.replaceAll(' ', '-');
                    dataLayer[name] = value;
                }

                window.dataLayer && window.dataLayer.push(dataLayer);
            }

            toString() {
                return this.toHtmlAttr();
            }

            click(value) {
                return this.set(GtmParams.PREFIX + 'click', value);
            }

            linkClick(value) {
                return this.set(GtmParams.PREFIX + 'link-click', value);
            }

            service(value) {
                return this.set(GtmParams.PREFIX + 'service', value);
            }

            page(value) {
                return this.set(GtmParams.PREFIX + 'page', value);
            }

            area(value) {
                return this.set(GtmParams.PREFIX + 'area', value);
            }

            type(value) {
                return this.set(GtmParams.PREFIX + 'type', value);
            }

            var1(value) {
                return this.set(GtmParams.PREFIX + 'var1', value);
            }

            var2(value) {
                return this.set(GtmParams.PREFIX + 'var2', value);
            }
        },

        getGTMPageName: function () {
            var pageName = '';
            if (window.location.hostname == 'forum.gamer.com.tw') {
                switch (window.location.pathname) {
                    case '/A.php':
                        return 'A��';
                    case '/B.php':
                        return 'B��';
                    case '/C.php':
                        return 'C��';
                    case '/Co.php':
                        return 'Co��';
                    case '/G1.php':
                        return '蝎曇虾���𤌍����𡑒”��';
                    case '/G2.php':
                        return '蝎曇虾������惩�批捆��';
                    case '/index.php':
                        return '�梢����襥��';
                    case '/myBoard.php':
                        return '��𤑳����襥��';
                    case '/search.php':
                        return '��𨅯�讠�鞉�𣈯�';
                    case '/post1.php':
                        return '���襥�踎�䔄����';
                    default:
                        return '';
                }
            }
            if (window.location.hostname == 'home.gamer.com.tw') {
                switch (window.location.pathname) {
                    case '/index.php':
                        return '�肟雿𨅯之撱�';
                    case '/artwork.php':
                    case '/creationDetail.php':
                        return '�肟雿𨀣���𣳇�';
                    case '/profile/my_board.php':
                        return '撠誩�𧢲�𤑳����襥�踎';
                    case '/profile/forum_post.php':
                        return '撠誩�见��襥���䔄銵券�';
                    case '/creation/coin_analysis.php':
                        return '�肟雿𡏭��敺�蝱_���⏚���钅�';
                    case '/creation/comment_manage_creation':
                        return '�肟雿𡏭��敺�蝱_���鰵��噼���_撠誩��';
                    case '/creation/dashboard.php':
                        return '�肟雿𡏭��敺�蝱_敺�蝱銝駁�';
                    default:
                        return '';
                }
            }
            if (window.location.hostname == 'gnn.gamer.com.tw') {
                switch (window.location.pathname) {
                    case '/index.php':
                        return 'GNN��𡑒”';
                    case '/gnn.php':
                        return 'GNN�批捆��';
                    default:
                        return '';
                }
            }
            if (window.location.hostname == 'guild.gamer.com.tw') {
                switch (window.location.pathname) {
                    case '/index.php':
                        return '�祆�憭批輒';
                    case '/guild.php':
                        return '�祆���';
                    case '/feed.php':
                        return '�祆���閙�讠�';
                    case '/post_detail.php':
                        return '�祆��鱓蝭����惩�批捆��';
                    default:
                        return '';
                }
            }
            if (window.location.hostname == 'www.gamer.com.tw') {
                switch (window.location.pathname) {
                    case '/index.php':
                    case '/index2.php':
                        return '擐㚚�';
                    default:
                        return '';
                }
            }
            if (window.location.hostname == 'prj.gamer.com.tw') {
                switch (window.location.pathname) {
                    case '/acg/acgEvent.php':
                        return '鞊鞉遛銝駁�屸�';
                    default:
                        return '';
                }
            }
            return pageName;
        }
    };

    Util.String = UtilString;
    Util.Number = UtilNumber;
    Util.Html = UtilHtml;
    Util.Api = UtilApi;
    Util.UserAgent = UtilUserAgent;
    Util.Pagination = UtilPagination;
    Util.Theme = UtilTheme;
    Util.Ga4 = UtilGa4;
    window.Util = Util;
})(jQuery, window);