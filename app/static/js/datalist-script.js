function applyDatalistBehavior(inputClass) {
    const inputs = document.querySelectorAll('.' + inputClass);

    inputs.forEach(input => {
        const datalistId = input.getAttribute('list');
        const datalist = document.getElementById(datalistId);
        let valueSelected = false;

        input.addEventListener("keydown", function(event) {
            if (event.keyCode === 9) { // Verifica se a tecla pressionada é a tecla Tab
                if (!valueSelected && input.value !== '') { // Ignora o preenchimento se o campo estiver vazio
                    const value = input.value;
                    const options = datalist.options;

                    for (let i = 0; i < options.length; i++) {
                        if (options[i].value.toLowerCase().startsWith(value.toLowerCase())) {
                            input.value = options[i].value;
                            valueSelected = true;
                            break;
                        }
                    }
                }
            } else {
                valueSelected = false;
            }
        });
    });
}
