/// <reference types="react-scripts" />

class WineOffer {
  supplierName: string;
  supplierEmail: string;
  linkedWineLwin: string;
  originalOfferText: string;
  producer: string;
  wineName: string;
  quantity: number;
  year: number;
  price: number;
  currency: string;
  isOWC: boolean;
  isOC: boolean;
  isIB: boolean;
  bottlesPerCase: number;
  bottleSize: string;
  bottleSizeNumerical: number;
  region: string;
  subRegion: string;
  colour: string;
  createdAt: string;
  id: string;
  logit_key: string;
  nb_key: string;
  svm_key: string;
  price_difference: number;
  offers_FK: string;
  price_difference: string;
}

class Transaction {
  transactions_id: number;
  vendorId: number;
  postingGroup: string;
  number: string;
  lwinNumber: string;
  description: string;
  measurementunit: string;
  quantity: number;
  directunitcost: number;
  amount: number;
  variantcode: number;
  postingdate: Date;
  purchaseinitials: string;
  offers_FK: string;
}
