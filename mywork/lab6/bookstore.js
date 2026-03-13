// Task 2: use database
db = db.getSiblingDB("bookstore")

// Task 3: insert first author
db.authors.insertOne({
  name: "Jane Austen",
  nationality: "British",
  bio: {
    short: "English novelist known for novels about the British landed gentry.",
    long: "Jane Austen was an English novelist whose works critique the British landed gentry."
  }
})

// Task 4: update to add birthday
db.authors.updateOne(
  { name: "Jane Austen" },
  { $set: { birthday: "1775-12-16" } }
)

// Task 5: insert four more authors
db.authors.insertMany([
{
  name: "Charles Dickens",
  nationality: "British",
  bio: { short: "Victorian novelist", long: "Famous for Oliver Twist." },
  birthday: "1812-02-07"
},
{
  name: "Mark Twain",
  nationality: "American",
  bio: { short: "American writer", long: "Author of Huckleberry Finn." },
  birthday: "1835-11-30"
},
{
  name: "Haruki Murakami",
  nationality: "Japanese",
  bio: { short: "Japanese novelist", long: "Known for surreal fiction." },
  birthday: "1949-01-12"
},
{
  name: "Gabriel Garcia Marquez",
  nationality: "Colombian",
  bio: { short: "Magical realism author", long: "Wrote One Hundred Years of Solitude." },
  birthday: "1927-03-06"
}
])

// Task 6: total count
db.authors.countDocuments()

// Task 7: British authors sorted by name
db.authors.find({ nationality: "British" }).sort({ name: 1 })