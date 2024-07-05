'use client'
import Image from "next/image";
import "@/styles/globals.css";
import { useState } from "react"
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Slider } from "@/components/ui/slider"


// /enrich/company

export default function Home() {

  const [domainList, setDomainList] = useState<string[]>([]);
  const [jobTitlesList, setJobTitlesList] = useState<string>("");
  const [useOnlyNewContacts, setUseOnlyNewContacts] = useState<boolean>(false)
  const [maxDollars, setMaxDollars] = useState<number>(50);

  const [responseFromBackend, setResponseFromBackend] = useState<string>("");

  const useEffect = () => {
    console.log("calling useEffect()");
  };

  const handleSubmitToBackend = async () => {
    const data = {
      domainList,
      jobTitlesList,
      useOnlyNewContacts,
      maxDollars
    }
    const jsonString = JSON.stringify(data, null, 2);
    console.log(jsonString);

    fetch( `${process.env.NEXT_PUBLIC_BACKEND_URL}/handler/hello`, {
        method : "POST",
        headers : { 'Content-Type': 'application/json' },
        body : jsonString,
      })
      .then(response => response.json())  // Convert to JSON
      .then(data => {
        setResponseFromBackend(JSON.stringify(data.organizations));  // Access the 'message' property
      })    
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24" >
      <div className="border flex z-10 w-full max-w-5xl items-center justify-center font-mono text-sm lg:flex">
        <Card className = "min-w-[400px] min-h-[400px] bg-gray-50 p-8">
            <CardHeader>
              <CardTitle>
                Auto-mailer tool
              </CardTitle>
            </CardHeader>
          <CardContent>
            <CardDescription className = "mb-4">
              Here is the card description and lorem ipsum dolor
            </CardDescription>
            <div className = "flex flex-col justify-center items-start py-2 my-3">
              <div className = "flex flex-row items-center justify-center py-1">
                <Checkbox onClick = {() => {setUseOnlyNewContacts(!useOnlyNewContacts)}} />
                <Label className = "px-2">Send to existing hubspot contacts?</Label>
              </div>
            </div>
            <div className="flex flex-col w-full max-w-sm items-center justify-center gap-1.5 my-3 py-2">
              <Label>Paste in the target domains here, separated by commas</Label>
              <Textarea className = "bg-gray-50" value={domainList} onChange={(e) => setDomainList(e.target.value)} />
            </div>
            <div className="flex flex-col w-full max-w-sm items-center justify-center gap-1.5 my-3 py-2">
              <Label>Paste in the target job titles here, separated by commas</Label>
              <Textarea className = "bg-gray-50" value={jobTitlesList} onChange={(e) => setJobTitlesList(e.target.value)} />
            </div>
            <div className="flex flex-col w-full max-w-sm items-center justify-center gap-1.5 my-3 py-2">
              <Label>Enter the maximum dollar value to spend (currently set to ${maxDollars})</Label>
              <Slider defaultValue= {[50]} max = {500} step = {10} onValueChange={(e) => {setMaxDollars(e[0])}} />
            </div>
            <div className = "flex justify-end">
              <Button onClick = {handleSubmitToBackend} className = "my-3 bg-gray-400">
                attempt to submit
              </Button>
            </div>
            <p>
              {responseFromBackend}
            </p>
          </CardContent>   
        </Card>
      </div>
    </main>
  );
}
