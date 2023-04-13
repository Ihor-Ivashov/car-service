var customer_field = document.getElementById("id_customer");
customer_field.addEventListener("change", function() {
  var customer = customer_field.value;
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/get_customer_cars/", true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  xhr.setRequestHeader("X-CSRFToken", csrftoken);

  xhr.onload = function() {
  if (xhr.status === 200) {
    var response = JSON.parse(xhr.responseText);
    var car_field = document.getElementById("id_car");
    car_field.innerHTML = ""; // очищаємо список варіантів
    var cars = response.cars;
    for (var i = 0; i < cars.length; i++) {
      var option = document.createElement("option");
      option.text = cars[i].name;
      option.value = cars[i].id;
      car_field.add(option);
    }
  }
  };
  xhr.send("customer_field=" + encodeURIComponent(customer));
});
