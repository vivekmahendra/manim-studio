import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("generate", "routes/generate.tsx"),
  route("examples", "routes/examples.tsx")
] satisfies RouteConfig;
