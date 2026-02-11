const imageUrl = record && record.image_public_id && cloudinary && typeof cloudinary.url === "function"
  ? cloudinary.url(record.image_public_id)
  : "";

console.log("gardening world")
