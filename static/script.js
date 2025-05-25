const regionSel = $('#region');
const zoneSel = $('#zone');
const sectorSel = $('#sector');
const routeSel = $('#route');

function sortByName(arr) {
    return arr.slice().sort((a, b) => a.name.localeCompare(b.name));
}

regionSel.append(data.map(r => `<option>${r.name}</option>`));

regionSel.on('change', () => {
    const region = data.find(r => r.name === regionSel.val());
    const zones = region.zones;
    zoneSel.empty().append(zones.map(z => `<option>${z.name}</option>`));
    zoneSel.trigger('change');
});

zoneSel.on('change', () => {
    const region = data.find(r => r.name === regionSel.val());
    const zone = region.zones.find(z => z.name === zoneSel.val());
    const sectors = zone.sectors;
    sectorSel.empty().append(sectors.map(s => `<option>${s.name}</option>`));
    sectorSel.trigger('change');
});

sectorSel.on('change', () => {
    const region = data.find(r => r.name === regionSel.val());
    const zone = region.zones.find(z => z.name === zoneSel.val());
    const sector = zone.sectors.find(s => s.name === sectorSel.val());
    const routes = sortByName(sector.routes)
    routeSel.empty().append(routes.map(r => `<option value="${r.name}">${r.name} (${r.grade})</option>`));
});

$('#logForm').on('submit', e => {
    e.preventDefault();
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            region: regionSel.val(),
            zone: zoneSel.val(),
            sector: sectorSel.val(),
            route: routeSel.val(),
            attempt: $('#attempt').val(),
            lead: $('#lead').is(':checked'),
            date: $('input[name="date"]').val(),
            comment: $('input[name="comment"]').val()
        })
    }).then(res => {
        if (!res.ok) alert('Failed to save');
    });
});

regionSel.trigger('change');
