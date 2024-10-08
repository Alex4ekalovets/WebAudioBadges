class t {
    constructor() {
        this.listeners = {}
    }
    on(t, e) {
        return this.listeners[t] || (this.listeners[t] = new Set),
        this.listeners[t].add(e),
        () => this.un(t, e)
    }
    once(t, e) {
        const s = this.on(t, e)
          , i = this.on(t, ( () => {
            s(),
            i()
        }
        ));
        return s
    }
    un(t, e) {
        this.listeners[t] && (e ? this.listeners[t].delete(e) : delete this.listeners[t])
    }
    unAll() {
        this.listeners = {}
    }
    emit(t, ...e) {
        this.listeners[t] && this.listeners[t].forEach((t => t(...e)))
    }
}
class e extends t {
    constructor(t) {
        super(),
        this.subscriptions = [],
        this.options = t
    }
    onInit() {}
    init(t) {
        this.wavesurfer = t,
        this.onInit()
    }
    destroy() {
        this.emit("destroy"),
        this.subscriptions.forEach((t => t()))
    }
}
const s = {
    lineWidth: 1,
    labelSize: 11
};
class i extends e {
    constructor(t) {
        super(t || {}),
        this.unsubscribe = () => {}
        ,
        this.onPointerMove = t => {
            if (!this.wavesurfer)
                return;
            const e = this.wavesurfer.getWrapper().getBoundingClientRect()
              , {width: s} = e
              , i = t.clientX - e.left
              , r = Math.min(1, Math.max(0, i / s))
              , n = Math.min(s - this.options.lineWidth - 1, i);
            this.wrapper.style.transform = `translateX(${n}px)`,
            this.wrapper.style.opacity = "1";
            const o = this.wavesurfer.getDuration() || 0;
            this.label.textContent = this.formatTime(o * r);
            const a = this.label.offsetWidth;
            this.label.style.transform = n + a > s ? `translateX(-${a + this.options.lineWidth}px)` : "",
            this.emit("hover", r)
        }
        ,
        this.onPointerLeave = () => {
            this.wrapper.style.opacity = "0"
        }
        ,
        this.options = Object.assign({}, s, t),
        this.wrapper = document.createElement("div"),
        this.label = document.createElement("span"),
        this.wrapper.appendChild(this.label)
    }
    static create(t) {
        return new i(t)
    }
    addUnits(t) {
        return `${t}${"number" == typeof t ? "px" : ""}`
    }
    onInit() {
        if (!this.wavesurfer)
            throw Error("WaveSurfer is not initialized");
        const t = this.wavesurfer.options
          , e = this.options.lineColor || t.cursorColor || t.progressColor;
        this.wrapper.setAttribute("part", "hover"),
        Object.assign(this.wrapper.style, {
            position: "absolute",
            zIndex: 10,
            left: 0,
            top: 0,
            height: "100%",
            pointerEvents: "none",
            borderLeft: `${this.addUnits(this.options.lineWidth)} solid ${e}`,
            opacity: "0",
            transition: "opacity .1s ease-in"
        }),
        this.label.setAttribute("part", "hover-label"),
        Object.assign(this.label.style, {
            display: "block",
            backgroundColor: this.options.labelBackground,
            color: this.options.labelColor,
            fontSize: `${this.addUnits(this.options.labelSize)}`,
            transition: "transform .1s ease-in",
            padding: "2px 3px"
        });
        const s = this.wavesurfer.getWrapper();
        s.appendChild(this.wrapper),
        s.addEventListener("pointermove", this.onPointerMove),
        s.addEventListener("pointerleave", this.onPointerLeave),
        this.unsubscribe = () => {
            s.removeEventListener("pointermove", this.onPointerMove),
            s.removeEventListener("pointerleave", this.onPointerLeave)
        }
    }
    formatTime(t) {
        return `${Math.floor(t / 60)}:${`0${Math.floor(t) % 60}`.slice(-2)}`
    }
    destroy() {
        super.destroy(),
        this.unsubscribe(),
        this.wrapper.remove()
    }
}
export {i as default};
