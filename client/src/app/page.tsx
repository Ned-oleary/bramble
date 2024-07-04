'use client'
import Image from "next/image";
import "@/styles/globals.css";
import { useState } from "react"
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card"

export default function Home() {

  const [state, setState] = useState<string>("default string")

  const useEffect = () => {
    console.log("calling useEffect()")
    console.log(state)
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="border flex z-10 w-full max-w-5xl items-center justify-center font-mono text-sm lg:flex">
        <Card className = "w-[400px] h-[400px] bg-gray-50">
          <CardHeader>
            <CardTitle>
              Here is the card title
            </CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>
              Here is the card description and lorem ipsum dolor
            </CardDescription>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
