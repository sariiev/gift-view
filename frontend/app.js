let chart = null

async function init() {
    await loadGifts()
    await loadModels()
    await loadChart()

    document.getElementById("gift").addEventListener("change", async () => {
        await loadModels()
        await loadChart()
    })

    document.getElementById("model").addEventListener("change", loadChart)
    document.getElementById("interval").addEventListener("change", loadChart)
}

async function loadGifts() {
    try {
        const res = await fetch("/gifts")

        if (!res.ok) throw new Error("Failed to load gifts")

        const data = await res.json()

        data.sort((a, b) => a.name.localeCompare(b.name))

        const select = document.getElementById("gift")

        data.forEach(gift => {
            const option = document.createElement("option")
            option.value = gift.name
            option.text = gift.name
            select.appendChild(option)
        })
    } catch (err) {
        console.error(err)
    }
}


async function loadModels() {
    try {
        const gift = document.getElementById("gift").value

        const res = await fetch(`/gifts/${encodeURIComponent(gift)}/models`)

        if (!res.ok) throw new Error("Failed to load models")

        const data = await res.json()

        data.sort((a, b) => a.rarity_percent - b.rarity_percent)

        const select = document.getElementById("model")

        select.innerHTML = '<option value="">All models</option>'

        data.forEach(model => {
            const option = document.createElement("option")
            option.value = model.name
            option.text = `${model.name} (${model.rarity_percent}%)`
            select.appendChild(option)
        })
    } catch (err) {
        console.error(err)
    }
}


async function loadChart() {
    try {
        // button.disabled = true
        // button.innerText = "Loading..."

        const gift = document.getElementById("gift").value
        const model = document.getElementById("model").value
        const interval = document.getElementById("interval").value

        if (!gift) return

        let url = `/gifts/${encodeURIComponent(gift)}/price-history?interval=${interval}`

        if (model) {
            url += `&model_name=${encodeURIComponent(model)}`
        }

        const res = await fetch(url)

        if (!res.ok) throw new Error("Failed to load chart data")

        const data = await res.json()

        const labels = data.map(x => x.timestamp)
        const prices = data.map(x => x.median_price)

        if (chart) {
            chart.destroy()
        }

        chart = new Chart(document.getElementById("chart"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Median Price",
                    data: prices,
                    tension: 0.2
                }]
            }
        })
    } catch (err) {
        console.error(err)
    } finally {
        // button.disabled = false
        // button.innerText = "Load"
    }
}


init()