function deleteStaple(stapleId) {
    fetch("/delete-staple", {
      method: "POST",
      body: JSON.stringify({ stapleId: stapleId }),
    }).then((_res) => {
      window.location.href = "/shoppinglist";
    });
  }

function deleteGrocery(groceryId) {
    fetch("/delete-grocery", {
      method: "POST",
      body: JSON.stringify({ groceryId: groceryId }),
    }).then((_res) => {
      window.location.href = "/shoppinglist";
    });
  }

  function checkStaple(stapleId) {
    fetch("/check-staple", {
      method: "POST",
      body: JSON.stringify({ stapleId: stapleId }),
    }).then((_res) => {
      window.location.href = "/shoppinglist";
    });
    }

