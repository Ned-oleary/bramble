'use client'
import Image from "next/image";
import "@/styles/globals.css";
import { useState } from "react"
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";


export default function Home() {

  const [toggle, setToggle] = useState<boolean>(true)

  const handleToggle = () => {
    setToggle(!toggle);
    console.log("calling handleToggle");
    console.log(toggle);
  }

  interface Association{
    to_id: number,
    associationCategory: string,
    associationTypeID: number
   }
  interface HubspotProperties{
    email: string,
    firstname: string,
    lastname: string,
    associations: Association[]
  }

  const useEffect = () => {
    console.log("calling useEffect()");
    console.log(toggle);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24" >
      <div className="border flex z-10 w-full max-w-5xl items-center justify-center font-mono text-sm lg:flex">
        <Card className = "w-[400px] h-[400px] bg-gray-50">
          <CardHeader>
            <CardTitle>
              Here is the card title
            </CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription className = "mb-4">
              Here is the card description and lorem ipsum dolor
            </CardDescription>
            <div className = "flex flex-col justify-center items-start m-1 p-1 border">
              <div className = "flex flex-row items-center justify-center py-1">
                <Checkbox onClick={handleToggle} />
                <Label className = "px-2">Here is some text</Label>
              </div>
              <div className = "flex flex-row items-center justify-center py-1">
                <Checkbox />
                <Label className = "px-2">Here is some text</Label>
              </div>
              <div className = "flex flex-row items-center justify-center py-1">
                <Checkbox />
                <Label className = "px-2">Here is some text</Label>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
