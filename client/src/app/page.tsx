'use client'
import Image from "next/image";
import "@/styles/globals.css";
import { useState } from "react"
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

// /enrich/company

export default function Home() {

  const [domain, setDomain] = useState<string>("");
  const [apolloOutput, setApolloOutput] = useState<string>("");

  // const handleToggle = () => {
  //   setToggle(!toggle);
  //   console.log("calling handleToggle");
  //   console.log(toggle);
  // }

  // interface Association{
  //   to_id: number,
  //   associationCategory: string,
  //   associationTypeID: number
  //  }
  // interface HubspotProperties{
  //   email: string,
  //   firstname: string,
  //   lastname: string,
  //   associations: Association[]
  // }

  const useEffect = () => {
    console.log("calling useEffect()");
  };

  const submitToApollo = async () => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/apollo/enrich/company`, {
      method: "POST", headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        choice: "bulk",
        domains: ["ssoready.com"]
      })
    });
    const data = await response.json();
    console.log((data.organizations)[0].industry);
    setApolloOutput((data.organizations)[0].industry); 
    return null;
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
                <Checkbox />
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
          <div className = "flex">
            <p> { apolloOutput } </p>
          </div>
          <Button onClick = {submitToApollo}>
              attempt to submit
          </Button>
        </Card>
      </div>
    </main>
  );
}
