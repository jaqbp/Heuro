export const testFunctions = [
  {
    id: 0,
    name: "Funkcja Rastrigina",
    formula: "f(x) = A * n + ∑ (x_i^2 - A * cos(2 * π * x_i))",
  },
  {
    id: 1,
    name: "Funkcja Bukina N.6",
    formula: "f(x, y) = 100 * √|y - 0.01*x^2| + 0.01*|x + 10|",
  },
  {
    id: 2,
    name: "Funkcja Rosenbrocka",
    formula: "f(x, y) = ∑(100 * (x_i+1 - x_i^2)^2 + (1 - x_i)^2)",
  },
  {
    id: 3,
    name: "Funkcja Himmelblau",
    formula: "f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2",
  },
  {
    id: 4,
    name: "Twoja własna funkcja",
    formula: "",
  },
  {
    id: 5,
    name: "Objective function",
    formula: "",
  },
];

export const algorithms = [
  { id: 0, name: "Algorytm GOA" },
  { id: 1, name: "Optymalizacja rojem cząstek (PSO)" },
  { id: 2, name: "Algorytm mrówkowy (ACO)" },
  { id: 3, name: "Algorytm optymalizacji kolonii nietoperzy" },
];
