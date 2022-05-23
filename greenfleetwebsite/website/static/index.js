function deleteAsset(assetId) {
  console.log("HI")
  fetch("/assets/delete-asset", {
    method: "POST",
    body: JSON.stringify({ assetId: assetId }),
  }).then((_res) => {
    window.location.href = "/assets";
  });
}

function editAsset(assetId) {
  fetch("/assets", {
    method: "POST",
    body: JSON.stringify({ assetId: assetId }),
  }).then((_res) => {
    window.location.href = "/assets/edit-asset/{{assetId}}";
  });
}

function deleteFleet(fleetId) {
  fetch("/fleets/delete-fleet", {
    method: "POST",
    body: JSON.stringify({ fleetId: fleetId }),
  }).then((_res) => {
    window.location.href = "/fleets";
  });
}

function deleteTech(techId) {
  fetch("/retrofits/delete-retrofit", {
    method: "POST",
    body: JSON.stringify({ techId: techId }),
  }).then((_res) => {
    window.location.href = "/retrofits";
  });
}

