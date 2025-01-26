import Chatbot from "@/components/Chatbot";
import Image from "next/image";

export default function Home() {
  return (
    <div className="grid p-4 gap-8">
      <header className="flex flex-col items-center justify-center gap-5">
        <h1 className="text-6xl font-bold ">Bussiness Chatbot</h1>
        <p>
          Ask about our products, services, or anything else you need help with.
        </p>
      </header>

      <main className="">
        <Chatbot />
      </main>
    </div>
  );
}
