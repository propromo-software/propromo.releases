# Propromo Releases

## Configuration

> This website uses "Method 4 - Hugo module" of [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod) for theming.

[hugo.yml](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation#sample-configyml)  

## Running the Development Server

To run this website locally for development, follow these steps:

1. **Prerequisites**
   - Install [Hugo](https://gohugo.io/installation) (extended version)
   - Install [Go](https://go.dev/dl) (required for Hugo modules)

2. **Clone the Repository**

   ```bash
   git clone https://github.com/propromo-org/propromo.releases.git
   cd propromo.releases
   ```

3. **Initialize Hugo Modules**

   ```bash
   hugo mod init github.com/propromo-software/propromo.releases
   hugo mod get -u
   hugo mod tidy
   ```

4. **Start the Development Server**

   ```bash
   hugo server -D
   ```

   The site will be available at [http://localhost:1313/](http://localhost:1313/)

## Create a New Post

```bash
hugo new posts/\<post-name\>.md --kind post
```
