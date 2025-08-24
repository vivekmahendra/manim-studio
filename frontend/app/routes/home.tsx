import type { Route } from "./+types/home";
import { Navigation } from "../components/Navigation";
import { Hero } from "../components/Hero";
import { Features } from "../components/Features";
import { HowItWorks } from "../components/HowItWorks";
import { Examples } from "../components/Examples";
import { Footer } from "../components/Footer";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "ManimStudio - Transform Ideas into Beautiful Math Animations" },
    { name: "description", content: "Create professional mathematical animations from plain English descriptions. Powered by AI and Manim, ManimStudio makes it easy to visualize complex mathematical concepts." },
    { property: "og:title", content: "ManimStudio - AI-Powered Math Animations" },
    { property: "og:description", content: "Transform mathematical concepts into beautiful animations with simple text prompts." },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: "summary_large_image" },
    { name: "twitter:title", content: "ManimStudio - Transform Ideas into Math Animations" },
    { name: "twitter:description", content: "Create professional mathematical animations from plain English. No coding required." },
  ];
}

export default function Home() {
  return (
    <>
      <Navigation />
      <Hero />
      <Features />
      <HowItWorks />
      <Examples />
      <Footer />
    </>
  );
}
