let app = Vue.createApp({
    data: function(){
        return {
            button_state: "--",
            base_url: window.location.origin,
            slider_value: 50,
            power_state: false,
            current_color: "-",
            className: "button",
        }
    },
    methods: {
        async toggle()
        {
            const headers = { 'Content-Type': 'multipart/form-data', 'accept': 'application/json' };
            const res = await axios.put(this.base_url + '/0/toggle', {}, { headers });
            console.log('Toggle bulb 0 res: ' + res.data.status);
            this.power_state = !this.power_state;
            this.update_button_status();
        },
        async turn_green()
        {
            const headers = { 'Content-Type': 'application/json', 'accept': 'application/json' };
            const rgb_value = {"red": 0, "green": 255, "blue": 0}
            const res = await axios.put(this.base_url + '/0/rgb', rgb_value, { headers });
            console.log('Toggle bulb 0 res: ' + res.data.status);
            this.current_color = "green";
            this.update_button_status();
        },
        async turn_red()
        {
            const headers = { 'Content-Type': 'application/json', 'accept': 'application/json' };
            const rgb_value = {"red": 255, "green": 0, "blue": 0}
            const res = await axios.put(this.base_url + '/0/rgb', rgb_value, { headers });
            console.log('Toggle bulb 0 res: ' + res.data.status);
            this.current_color = "red";
            this.update_button_status();
        },
        async changeFoo()
        {
            this.slider_value = this.sliderVal;
            const headers = { 'Content-Type': 'application/json', 'accept': 'application/json' };
            const res = await axios.put('/0/brightness', {}, { headers, params: {"value": this.slider_value} });
            console.log('Set bulb 0 brightness to ' + this.slider_value + ' res: ' + res.data.status);
        },
        update_button_status()
        {
            if (this.power_state)
            {
                this.className = "button button-" + this.current_color;
                this.button_state = "Turn OFF";
            }
            else
            {
                this.className = "button";
                this.button_state = "Turn ON";
            }
        }
    },
    created: async function()
    {
            const headers = { 'Content-Type': 'application/json', 'accept': 'application/json' };
            const res = await axios.get('/0/state', {}, { headers });
            this.power_state = res.data.power
            this.current_color = res.data.color;
            this.update_button_status();
            this.sliderVal = res.data.bright;
    }
})
app.mount('#app')