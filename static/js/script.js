// Get the references
const metricRadio = document.getElementById("metric");
const imperialRadio = document.getElementById("imperial");
const heightUnit = document.getElementById("height-unit");
const weightUnit = document.getElementById("weight-unit");
const heightValue = document.getElementById("height-value");
const weightValue = document.getElementById("weight-value");
const results = document.getElementById("bmi-result");
const btn = document.getElementById("btn");

// Update units
const updateUnits = () => {
  if (metricRadio.checked) {
    heightUnit.textContent = "cm";
    weightUnit.textContent = "kg";
  } else if (imperialRadio.checked) {
    heightUnit.textContent = "in";
    weightUnit.textContent = "lb";
  }
};

metricRadio.addEventListener("change", updateUnits);
imperialRadio.addEventListener("change", updateUnits);

// Calculate BMI
const calculateBMI = (e) => {
  e.preventDefault();
  const height = parseFloat(heightValue.value);
  const weight = parseFloat(weightValue.value);
  let bmi = 0;
  let bmiDescription = "";

  if (metricRadio.checked) {
    bmi = (weight / (height / 100) ** 2).toFixed(2);
  } else if (imperialRadio.checked) {
    bmi = ((weight / height ** 2) * 703).toFixed(2);
  }

  switch (true) {
    case bmi < 18.5:
      bmiDescription = "Your BMI suggests you're underweight";
      break;
    case bmi >= 18.5 && bmi < 24.9:
      bmiDescription = "Your BMI suggests you're a healthy weight";
      break;
    case bmi >= 25.0 && bmi < 29.0:
      bmiDescription = "Your BMI suggests you're overweight";
      break;
    case bmi >= 30.0:
      bmiDescription = "Your BMI suggests you're obese";
      break;
    default:
      bmiDescription = "Invalid BMI value";
  }

  results.textContent = `Your BMI is ${bmi}. ${bmiDescription}.`;
};

btn.addEventListener("click", (e) => calculateBMI(e));

