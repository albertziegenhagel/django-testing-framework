(function () {
    function formatLocalDatetime(date) {
        if (!date || typeof date.getTime !== "function" || Number.isNaN(date.getTime())) {
            return "";
        }

        return new Intl.DateTimeFormat(undefined, {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        }).format(date);
    }

    function getLocalTimezoneName() {
        return Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    }

    function formatTooltipDatetime(date) {
        if (!date || typeof date.getTime !== "function" || Number.isNaN(date.getTime())) {
            return "";
        }

        return new Intl.DateTimeFormat(undefined, {
            dateStyle: "full",
            timeStyle: "long",
        }).format(date);
    }

    function setLocalDatetimeTooltip(element, date) {
        if (!element) {
            return;
        }

        const formatted = formatTooltipDatetime(date);
        const timezone = getLocalTimezoneName();
        element.title = formatted
            ? (timezone ? `${formatted} (${timezone})` : formatted)
            : "";
    }

    function formatLocalDatetimes(root) {
        const scope = root || document;
        const elements = scope.querySelectorAll
            ? scope.querySelectorAll("time[data-local-datetime]")
            : [];

        elements.forEach(function (element) {
            const isoValue = element.dataset.localDatetime;
            const date = new Date(isoValue);

            if (Number.isNaN(date.getTime())) {
                return;
            }

            const formatted = formatLocalDatetime(date);
            const timezone = getLocalTimezoneName();

            element.textContent = formatted;
            setLocalDatetimeTooltip(element, date);
        });
    }

    if (typeof document !== "undefined") {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", function () {
                formatLocalDatetimes(document);
            });
        } else {
            formatLocalDatetimes(document);
        }
    }

    if (typeof module !== "undefined" && module.exports) {
        module.exports = {
            formatLocalDatetime,
            formatLocalDatetimes,
            formatTooltipDatetime,
            getLocalTimezoneName,
            setLocalDatetimeTooltip,
        };
    } else if (typeof window !== "undefined") {
        window.formatLocalDatetime = formatLocalDatetime;
        window.formatLocalDatetimes = formatLocalDatetimes;
        window.getLocalTimezoneName = getLocalTimezoneName;
        window.setLocalDatetimeTooltip = setLocalDatetimeTooltip;
    }
})();
