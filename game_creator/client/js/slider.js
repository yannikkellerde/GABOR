const inputs = document.querySelectorAll(".slider_input");
const labels = document.querySelectorAll(".slider_label");

for (var i=0;i<=inputs.length;i++){
    const input = inputs[i];
    const label = labels[i];
    const maxval = Number(input.getAttribute("data-max"));
    const eventfunc = event => {
        const value = Number(input.value) / 100;
        input.style.setProperty("--thumb-rotate", `${value * 720}deg`);
        const real_val = Math.round(value * maxval)
        label.innerHTML = real_val;
        input.setAttribute("data-value",real_val)
    }
    eventfunc();
    input.addEventListener("input", eventfunc);
}