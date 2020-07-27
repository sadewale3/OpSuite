import axios from "axios";

let development = process.env.NODE_ENV !== "production";

const httpClient = axios.create({
  baseURL: development
    ? "http://localhost:9008/api/v1"
    : "http://opsuite:9008/api/v1",
  headers: {
    "Content-Type": "application/json"
  }
});

export default httpClient;
