import React, { useContext } from 'react'
import { ShopContext } from '../Context/ShopContext'
import { useParams } from 'react-router-dom';
import Breadcrum from '../Components/Breadcrums/Breadcrum';
import BidDisplay from '../Components/BidDisplay/BidDisplay';
import DescriptionBox from '../Components/DescriptionBox/DescriptionBox';
import RelatedProducts from '../Components/RelatedProducts/RelatedProducts';
import ProductDisplay from '../Components/ProductDisplay/ProductDisplay';



const Product = () => {
  const {all_product}=useContext(ShopContext);
  const {productId}=useParams();
  const product=all_product.find((e)=> e.id===Number(productId));

  return (
    <div>
        <Breadcrum product={product} />
        {/* <BidDisplay product={product} /> */}
        <BidDisplay product={product} />
        <DescriptionBox/>
        <RelatedProducts/>
    </div>
  )
}

export default Product