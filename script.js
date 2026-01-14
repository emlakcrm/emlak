// ====== MÜÞTERÝ LÝSTESÝ (Local Storage) =======
let customerList = JSON.parse(localStorage.getItem("customers")) || [];

function saveCustomers() {
    localStorage.setItem("customers", JSON.stringify(customerList));
}

// ====== MÜÞTERÝ EKLE =======
function addCustomer() {
    let name = document.getElementById("name").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let note = document.getElementById("note").value.trim();

    if (name === "" || phone === "") {
        alert("Ýsim ve telefon zorunludur!");
        return;
    }

    customerList.push({ name, phone, note });
    saveCustomers();
    loadCustomers();

    document.getElementById("name").value = "";
    document.getElementById("phone").value = "";
    document.getElementById("note").value = "";

    alert("Müþteri eklendi!");
}

// ====== MÜÞTERÝ LÝSTESÝNÝ YÜKLE =======
function loadCustomers() {
    let listArea = document.getElementById("customerList");
    listArea.innerHTML = "";

    customerList.forEach((c, index) => {
        listArea.innerHTML += `
            <div class="list-item">
                <b>${c.name}</b><br>
                Tel: ${c.phone}<br>
                Not: ${c.note || "-"} <br><br>
                <button onclick="deleteCustomer(${index})">Sil</button>
            </div>
        `;
    });
}
loadCustomers();

// ====== MÜÞTERÝ SÝL =======
function deleteCustomer(index) {
    if (confirm("Bu müþteriyi silmek istiyor musun?")) {
        customerList.splice(index, 1);
        saveCustomers();
        loadCustomers();
    }
}

// ===== EXCEL'E AKTAR (CSV) =====
function exportExcel() {
    let csv = "Ýsim,Telefon,Not\n";

    customerList.forEach(c => {
        csv += ${c.name},${c.phone},${c.note}\n;
    });

    let blob = new Blob([csv], { type: "text/csv" });
    let url = URL.createObjectURL(blob);

    let a = document.createElement("a");
    a.href = url;
    a.download = "MusteriListesi.csv";
    a.click();

    URL.revokeObjectURL(url);
}