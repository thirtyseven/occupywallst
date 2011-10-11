
var index_init;

(function() {
    "use strict";

    var is_working = false;
    var stocks = ["^DJI"];//, "^GSPC","^IXIC"];
    var fullnames = { "^DJI" : "Dow Jones Index", "^GSPC": "S&P 500", "^IXIC": "NASDAQ" };

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
            plot_stock_data(data.results[0]);
        });
    }

    function plot_stock_data(data) {
        var div = $("#stock-chart");
        var occ_start_time = (new Date(2011, 8, 17)).getTime();
        var end_time = data.series[data.series.length-1][0];
        var series = [{
            label: fullnames[data.symb],
            data: data.series
        }];
        var plot = $.plot(div, series, {
            yaxes: [
                { position: "left",
                  tickFormatter: function(val, axis) {
                    return (val/100.0);
                  },
                },
                {
                    position: "right",
                    show: true,
                    tickFormatter: function(val, axis) {
                        return val + "%";
                    }

                } ],
            xaxis: {
                //ticks: [ 2, end_time ],
                tickFormatter: function(val, axis) {
                    if (val >= data.dates.length) { return false; }
                    var date = new Date(data.dates[val]);
                    var day = date.getDate();
                    var month = date.getMonth()+1;
                    return month + "/" + day;
                }
            }
        });
        function percent_trans(p) {
            var base = data.series[2][1];
            return (p-base)*100.0/base;
        }
        var yaxis = plot.getAxes().yaxis;
        var min = percent_trans(yaxis.min);
        var max = percent_trans(yaxis.max);
        var y2axis = plot.getOptions().yaxes[1];
        y2axis.min = min;
        y2axis.max = max;
        plot.setupGrid();
        plot.draw();
    }


    // export stuff
    index_init = init;

})();
