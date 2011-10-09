
var index_init;

(function() {
    "use strict";

    var is_working = false;
    var stocks = ["^DJI", "^GSPC","^IXIC"];
    var fullnames = { "^DJI" : "DOW", "^GSPC": "S&P 500", "^IXIC": "NASDAQ" };

    function init(args) {
        $(window).scroll(function(ev) {
            if (is_working)
                return;
            $("#archives article.unloaded").each(function() {
                if ($(this).scrolledToShow(250)) {
                    $(this).removeClass("unloaded");
                    $(".loady", this).fadeIn();
                    load_article($(this));
                    return false;
                }
            });
        }).scroll();
        get_stock_data();
    }

    function load_article(article) {
        is_working = true;
        api("/api/safe/article_get/", {
            "article_slug": article.attr("id")
        }, function(data) {
            is_working = false;
            if (data.status == "OK") {
                article.replaceWith($(data.results[0].html));
            } else {
                $(".loady", article).parent().text(data.message);
            }
        }).error(function(err) {
            is_working = false;
            $(".loady", article).parent().text(err.status + ' ' + err.statusText);
        });
    }

    function get_stock_data() {
        $.getJSON("/api/safe/stock_data_get/", { "symbols": stocks.join(":")}, function(data) {
            console.log(data);
            plot_stock_data(data.results);
        });
    }

    function plot_stock_data(arr) {
        var div = $("#stock-chart");
        var series = arr.map(function(item, i) {
            return {
                label: fullnames[item[0]],
            data: item[1]
            };
        });
        console.log(arr);
        console.log(series);
        $.plot(div, series, {
            yaxis: {
                tickFormatter: function(val, axis) {
                    return val + "%";
                }
            },
            xaxis: {
                mode: "time",
                timeformat: "%m/%d"
            }
        });
    }


    // export stuff
    index_init = init;

})();
