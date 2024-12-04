CREATE TABLE vendors (
    VendorNumber INT NOT NULL PRIMARY KEY,
    VendorName VARCHAR(255)
);

CREATE TABLE inventory (
	InventoryId VARCHAR(255) NOT NULL PRIMARY KEY,
	Store INT,
	Brand INT,
	Description VARCHAR(255),
	Size VARCHAR(255)
);

CREATE TABLE beginvfinal12312016 (
    InventoryId VARCHAR(255),
    City VARCHAR(255),
    onHand INT,
    Price DECIMAL(10, 2),
    startDate DATE,
	FOREIGN KEY (InventoryId) REFERENCES inventory(InventoryId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE endinvfinal12312016 (
    InventoryId VARCHAR(255),
    City VARCHAR(255),
    onHand INT,
    Price DECIMAL(10, 2),
    endDate DATE,
	FOREIGN KEY (InventoryId) REFERENCES inventory(InventoryId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE purchasesfinal12312016 (
    InventoryId VARCHAR(255),
    VendorNumber INT,
    PONumber INT,
    PODate DATE,
    ReceivingDate DATE,
    InvoiceDate DATE,
    PayDate DATE,
    PurchasePrice DECIMAL(10, 2),
    Quantity INT,
    Dollars DECIMAL(10, 2),
    Classification INT,
	FOREIGN KEY (VendorNumber) REFERENCES vendors(VendorNumber)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
	FOREIGN KEY (InventoryId) REFERENCES inventory(InventoryId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE invoicepurchases12312016 (
    VendorNumber INT,
    InvoiceDate DATE,
    PONumber INT,
    PODate DATE,
    PayDate DATE,
    Quantity INT,
    Dollars DECIMAL(10, 2),
    Freight DECIMAL(10, 2),
	FOREIGN KEY (VendorNumber) REFERENCES vendors(VendorNumber)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE salesfinal12312016 (
    InventoryId VARCHAR(255),
    SalesQuantity INT,
    SalesDollars DECIMAL(10, 2),
    SalesPrice DECIMAL(10, 2),
    SalesDate DATE,
    Volume INT,
    Classification INT,
    ExciseTax DECIMAL(10, 2),
    VendorNo INT,
	FOREIGN KEY (VendorNo) REFERENCES vendors(VendorNumber)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
	FOREIGN KEY (InventoryId) REFERENCES inventory(InventoryId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);