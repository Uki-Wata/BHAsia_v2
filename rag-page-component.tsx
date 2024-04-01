
import { Button } from "@/components/ui/button"


export function RagComponent() {
  return (
    <div className="flex flex-col h-screen">
      <header className="flex items-center justify-center h-14 border-b px-4 sm:h-16 md:px-6">
        <div className="flex items-center gap-2 text-sm font-semibold tracking-wider uppercase">

          shadcn
        </div>
      </header>
      <main className="flex-1 overflow-y-auto">
        <div className="container grid max-w-5xl items-start gap-6 px-4 py-6 mx-auto md:gap-10 md:px-6 lg:py-12">
          <div className="flex flex-col gap-4">
            <div className="grid w-full rounded-lg border border-gray-200 bg-white overflow-hidden dark:border-gray-800 dark:bg-gray-950">
              <img
                alt="Cover image"
                className="object-cover w-full h-96"
                height="400"
                src="/placeholder.svg"
                style={{
                  aspectRatio: "1200/400",
                  objectFit: "cover",
                }}
                width="1200"
              />
            </div>
            <div className="grid w-full rounded-lg border border-gray-200 bg-white p-6 space-y-4 dark:border-gray-800 dark:bg-gray-950 dark:space-y-2">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Welcome to the shadcn</h1>
              <p className="max-w-3xl text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                The definitive toolkit for crafting stunning interfaces.
              </p>
            </div>
            <div className="grid w-full rounded-lg border border-gray-200 bg-white p-6 space-y-4 dark:border-gray-800 dark:bg-gray-950 dark:space-y-2">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Welcome to the shadcn</h1>
              <p className="max-w-3xl text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                The definitive toolkit for crafting stunning interfaces.
              </p>
            </div>
            <div className="grid w-full rounded-lg border border-gray-200 bg-white p-6 items-center justify-center dark:border-gray-800 dark:bg-gray-950">
              shadcn
            </div>
          </div>
        </div>
      </main>
      <footer className="flex items-center border-t px-4 sm:px-6">
        <div className="container flex items-center justify-between h-14 md:h-16">
          <div className="flex gap-4 w-full">
            <Input className="max-w-xs flex-1" placeholder="Type your email" type="email" />
            <Input className="max-w-xs flex-1" placeholder="Type your email" type="email" />
            <Input className="max-w-xs flex-1" placeholder="Type your email" type="email" />
          </div>
          <Button className="ml-4 md:ml-6">Subscribe</Button>
        </div>
      </footer>
    </div>
  )}
