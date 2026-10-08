const form = document.querySelector("#calculator-form");
const firstInput = document.querySelector("#first-number");
const secondInput = document.querySelector("#second-number");
const resultEquation = document.querySelector("#result-equation");
const resultValue = document.querySelector("#result-value");
const errorMessage = document.querySelector("#error-message");

const operationSymbols = {
  "+": "+",
  "-": "−",
  "*": "×",
  "/": "÷",
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.hidden = true;

  if (firstInput.value.trim() === "" || secondInput.value.trim() === "") {
    showError("Enter both numbers to get a result.");
    return;
  }

  const first = Number(firstInput.value);
  const second = Number(secondInput.value);
  if (!Number.isFinite(first) || !Number.isFinite(second)) {
    showError("Enter two valid, finite numbers.");
    return;
  }

  const operation = form.elements.operation.value;
  resultValue.textContent = "...";
  resultEquation.textContent = "Working it out in Python";

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ first, second, operation }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The calculation could not be completed.");
    }

    resultEquation.textContent = `${formatNumber(first)} ${operationSymbols[operation]} ${formatNumber(second)} =`;
    resultValue.textContent = data.formatted_result;
  } catch (error) {
    resultValue.textContent = "—";
    resultEquation.textContent = "No result yet.";
    showError(error.message || "Could not reach the Python server. Is it still running?");
  }
});

function formatNumber(value) {
  return new Intl.NumberFormat(undefined, { maximumSignificantDigits: 12 }).format(value);
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}